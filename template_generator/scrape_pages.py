from playwright.sync_api import sync_playwright
import os

URLS = {
    "amazon": "https://www.amazon.com",
    "ebay": "https://www.ebay.com",
    "target": "https://www.target.com/",
    #"walmart": "https://www.walmart.com",
    #"shein": "https://www.shein.com/",
    #"homedepot": "https://www.homedepot.com/",
    #"bestbuy":"https://www.bestbuy.com/"
}

os.makedirs("raw_html", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for name, url in URLS.items():
        print(f"Scraping {url}")
        page.goto(url, timeout=60000)
        page.wait_for_load_state("load")
        html = page.content()
        with open(f"raw_html/{name}.html", "w", encoding="utf-8") as f:
            f.write(html)
    
    browser.close()