import os
import json
from datetime import datetime
from playwright.sync_api import sync_playwright

def capture_gui(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Take a screenshot
        screenshot = page.screenshot(full_page=True)
        
        # Define target element selectors
        TARGET_ELEMENTS = {
            "button": "button, input[type='button'], input[type='submit']",
            "input": "input[type='text'], input[type='search'], input[type='email'], textarea",
            "link": "a",
            "dropdown": "select",
            "checkbox": "input[type='checkbox']",
            "radio": "input[type='radio']",
            "searchbox": "input[type='search'], .search-box, .search-input",
        }

        elements = []

        # Extract all matching elements
        for element_type, selector in TARGET_ELEMENTS.items():
            element_handles = page.query_selector_all(selector)
            for el in element_handles:
                box = el.bounding_box()
                if not box:  # Skip hidden/invisible elements
                    continue

                # Get text (if any)
                text = el.evaluate("el => el.innerText || el.value || el.placeholder || ''")

                elements.append({
                    "type": element_type,
                    "label": text.strip() if text else None,
                    "bbox": [box["x"], box["y"], box["width"], box["height"]],
                    "selector": selector,
                })

        browser.close()

        return elements, screenshot

def save_capture(elements, screenshot):
    # Create output directory
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join("captures", timestamp)
    os.makedirs(output_dir, exist_ok=True)

    # Save elements list as JSON
    json_path = os.path.join(output_dir, "elements.json")
    with open(json_path, "w") as f:
        json.dump(elements, f, indent=2)

    # Save screenshot image
    image_path = os.path.join(output_dir, "screenshot.png")
    with open(image_path, "wb") as f:
        f.write(screenshot)

    print(f"Saved capture to: {output_dir}")
    return output_dir