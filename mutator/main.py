import os, asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse
from mutator import add_distractor, shuffle_siblings

async def main():
    # Step 1: Scrape html
    url = "https://www.google.com"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        original_html = await page.content()
        await browser.close()

    # Extract domain name for folder
    domain = urlparse(url).netloc.split('.')[-2]  # 'google' from 'www.google.com'
    output_dir = os.path.join(os.getcwd(), domain)
    os.makedirs(output_dir, exist_ok=True)

    # Save original HTML
    original_path = os.path.join(output_dir, f"{domain}_original.html")
    with open(original_path, "w", encoding='utf-8') as f:
        f.write(original_html)
    
    # Add distractor
    distracted_html = add_distractor(original_html, 0.5)
    filename = f"{domain}_distracted.html"
    with open(os.path.join(output_dir, filename), "w", encoding='utf-8') as f:
        f.write(distracted_html)

    # Shuffle siblings
    shuffled_html = shuffle_siblings(original_html)
    filename = f"{domain}_shuffled.html"
    with open(os.path.join(output_dir, filename), "w", encoding='utf-8') as f:
        f.write(shuffled_html)

if __name__ == '__main__':
    asyncio.run(main())