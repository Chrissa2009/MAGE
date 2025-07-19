from playwright.sync_api import sync_playwright
import os

os.makedirs("screenshots", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    for filename in os.listdir("clean_html"):
        path = f"clean_html/{filename}"
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        
        page.set_content(html, wait_until="domcontentloaded")
        page.screenshot(path=f"screenshots/{filename}.png", full_page=True)
    
    browser.close()
