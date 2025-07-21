from collections import defaultdict
import os, asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse
from mutator import add_distractor, shuffle_siblings

MUTATION_MAX_FREQ = {'distractor':10, 'shuffle':10, "original": 1}
DISTRACTOR_PERCENTAGE = 0.5
URLS = ['https://www.google.com']

async def main():
    data_dir = os.path.join(os.getcwd(), 'data')
    os.makedirs(data_dir, exist_ok=True)
    # Scrape HTML
    for url in URLS:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            original_html = await page.content()
            await browser.close()

        # Make folders
        domain = urlparse(url).netloc.split('.')[-2]
        domain_dir = os.path.join(data_dir, domain)
        os.makedirs(domain_dir, exist_ok=True)
        for mutation in MUTATION_MAX_FREQ:
            os.makedirs(os.path.join(domain_dir, mutation), exist_ok=True)
        
        # Perform mutations
        mutation_to_htmls = defaultdict(set)
        for mutation, frequency in MUTATION_MAX_FREQ.items():
            for i in range(frequency):
                if mutation == 'distractor':
                    mutated_html = add_distractor(original_html, DISTRACTOR_PERCENTAGE)
                elif mutation == "shuffle":
                    mutated_html = shuffle_siblings(original_html)
                elif mutation == "original":
                    mutated_html = original_html
                else:
                    raise Exception("Unsupported mutation")
                if mutated_html not in mutation_to_htmls[mutation]:
                    filename = f"{domain}_{mutation}_{i}.html"
                    with open(os.path.join(domain_dir, mutation, filename), "w", encoding='utf-8') as f:
                        f.write(mutated_html)
                    mutation_to_htmls[mutation].add(mutated_html)

if __name__ == '__main__':
    asyncio.run(main())