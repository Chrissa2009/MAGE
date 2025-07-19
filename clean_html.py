from bs4 import BeautifulSoup
import os

os.makedirs("clean_html", exist_ok=True)

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    # Remove unwanted elements: keep <style>, <link rel="stylesheet">, etc.
    for tag in soup(["script", "noscript", "svg", "iframe"]):
        tag.decompose()

    # Keep layout-related inline styles (e.g. for flex/grid display)
    layout_tags = {"div", "li", "ul", "img", "section", "span"}
    for tag in soup(True):
        if tag.name not in layout_tags and "style" in tag.attrs:
            del tag.attrs["style"]

    return soup.prettify()

for filename in os.listdir("raw_html"):
    with open(f"raw_html/{filename}", "r", encoding="utf-8") as f:
        raw = f.read()

    clean = clean_html(raw)

    with open(f"clean_html/{filename}", "w", encoding="utf-8") as f:
        f.write(clean)