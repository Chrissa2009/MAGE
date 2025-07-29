import os, asyncio, csv, time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
from mutator import add_distractor, shuffle_siblings
from tqdm import tqdm as base_tqdm

# ------------ Config ------------
MUTATION_MAX_FREQ = {'distractor': 10, 'shuffle': 10, 'original': 1}
DISTRACTOR_PERCENTAGE = 0.5
OUTPUT_DIR = os.path.join(os.getcwd(), 'data')
SCRAPE_TIMEOUT_MILLIS = 60000
MAX_FETCH_WORKERS = min(10, os.cpu_count() * 2)
MAX_MUTATE_SCHEDULERS = 2
MAX_WRITE_SCHEDULERS = 2
THREAD_POOL_SIZE = os.cpu_count()
WEBSITE_CONFIG = 'top_100_websites.csv'

# ------------ Read URLs ------------
def get_urls(config):
    urls = []
    csv_file_path = os.path.join(os.getcwd(), config)
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            urls.append(row['URL'])
    return urls

def block_unnecessary_resources(route):
    if route.request.resource_type in ["image", "font", "stylesheet"]:
        return route.abort()
    return route.continue_()

# ------------ Mutation Task → Write Queue ------------
def run_mutation_task(domain, mutation, html, index, write_queue, loop, mutate_bar):
    if mutation == 'distractor':
        mutated_html = add_distractor(html, DISTRACTOR_PERCENTAGE)
    elif mutation == 'shuffle':
        mutated_html = shuffle_siblings(html)
    elif mutation == 'original':
        mutated_html = html
    else:
        return

    asyncio.run_coroutine_threadsafe(
        write_queue.put((domain, mutation, index, mutated_html)),
        loop
    )

    mutate_bar.update(1)

def enqueue_mutation_trials(domain, html, executor, write_queue, loop, mutate_bar):
    for mutation, count in MUTATION_MAX_FREQ.items():
        for i in range(count):
            executor.submit(run_mutation_task, domain, mutation, html, i, write_queue, loop, mutate_bar)

def run_write_task(domain, mutation, index, html, write_bar):
    try:
        mutation_dir = os.path.join(OUTPUT_DIR, domain, mutation)
        os.makedirs(mutation_dir, exist_ok=True)
        filename = f"{domain}_{mutation}_{index}.html"
        path = os.path.join(mutation_dir, filename)
        with open(path, "w", encoding='utf-8') as f:
            f.write(html)
    except Exception as e:
        print(f"[ERROR] Failed to write {domain} {mutation}_{index}: {e}")
    write_bar.update(1)

def enqueue_write(domain, mutation, index, html, executor, write_bar):
    executor.submit(run_write_task, domain, mutation, index, html, write_bar)

async def write_consumer(executor, write_queue, write_bar):
    while True:
        domain, mutation, index, html = await write_queue.get()
        enqueue_write(domain, mutation, index, html, executor, write_bar)
        write_queue.task_done()

# ------------ Fetch HTML → Queue ------------
async def fetch_and_enqueue(url, context, queue, domain_bar):
    try:
        page = await context.new_page()
        await page.route("**/*", lambda route: asyncio.ensure_future(block_unnecessary_resources(route)))
        await page.goto(url, wait_until='domcontentloaded', timeout=SCRAPE_TIMEOUT_MILLIS)
        html = await page.content()
        await page.close()
        domain = urlparse(url).netloc.split('.')[-2]
        await queue.put((domain, html))
        domain_bar.update(1)
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")

# ------------ Mutation Consumer ------------
async def mutation_consumer(fetch_queue, executor, write_queue, loop, mutate_bar):
    while True:
        domain, html = await fetch_queue.get()
        enqueue_mutation_trials(domain, html, executor, write_queue, loop, mutate_bar)
        fetch_queue.task_done()

# ------------ Main ------------
async def main():
    print(f"[INFO] MAX_FETCH_WORKERS: {MAX_FETCH_WORKERS}")
    print(f"[INFO] MAX_MUTATE_SCHEDULERS: {MAX_MUTATE_SCHEDULERS}")
    print(f"[INFO] MAX_WRITE_SCHEDULERS: {MAX_WRITE_SCHEDULERS}")
    print(f"[INFO] THREAD_POOL_SIZE: {THREAD_POOL_SIZE}")
    print(f"[INFO] WEBSITE_CONFIG: {WEBSITE_CONFIG}")

    total_start = time.time()

    async with async_playwright() as p:
        # Init
        init_start = time.time()
        urls = get_urls(WEBSITE_CONFIG)
        total_urls = len(urls)
        total_mutations = total_urls * sum(MUTATION_MAX_FREQ.values())

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        fetch_queue = asyncio.Queue()
        write_queue = asyncio.Queue()
        executor = ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE)
        loop = asyncio.get_running_loop()

        fetch_bar = base_tqdm(total=total_urls, desc="Fetching", position=0)
        mutate_bar = base_tqdm(total=total_mutations, desc="Mutating", position=1)
        write_bar = base_tqdm(total=total_mutations, desc="Writing", position=2)

        consumers = [
            asyncio.create_task(mutation_consumer(fetch_queue, executor, write_queue, loop, mutate_bar))
            for _ in range(MAX_MUTATE_SCHEDULERS)
        ]
        writers = [
            asyncio.create_task(write_consumer(executor, write_queue, write_bar))
            for _ in range(MAX_WRITE_SCHEDULERS)
        ]

        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        sem = asyncio.Semaphore(MAX_FETCH_WORKERS)
        init_end = time.time()

        async def bounded_fetch(url):
            async with sem:
                await fetch_and_enqueue(url, context, fetch_queue, fetch_bar)

        # 1. Fetch timing
        fetch_start = time.time()
        await asyncio.gather(*[bounded_fetch(url) for url in urls])
        fetch_end = time.time()

        # 2. Mutation + write
        await fetch_queue.join()
        await write_queue.join()

        # Cleanup
        for c in consumers:
            c.cancel()
        for w in writers:
            w.cancel()
        await browser.close()
        executor.shutdown(wait=True)

        fetch_bar.close()
        mutate_bar.close()
        write_bar.close()

    total_end = time.time()

    # Summaries
    print(f"[SUMMARY] Initialization duration: {init_end - init_start:.2f}s")
    print(f"[SUMMARY] Fetch duration: {fetch_end - fetch_start:.2f}s")
    print(f"[SUMMARY] Mutation+Write duration: {total_end - total_start - (fetch_end - fetch_start) - (init_end - init_start):.2f}s")
    print(f"[SUMMARY] Total runtime: {total_end - total_start:.2f}s")

if __name__ == '__main__':
    asyncio.run(main())
