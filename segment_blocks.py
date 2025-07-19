from bs4 import BeautifulSoup

def extract_main_components(html):
    soup = BeautifulSoup(html, "html.parser")

    blocks = {
        "nav": soup.find("nav"),
        "header": soup.find("header"),
        "main": soup.find("main"),
        "footer": soup.find("footer"),
    }

    return {k: str(v) for k, v in blocks.items() if v}

# Use later for annotation or mutation