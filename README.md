# MAGE

**MAGE (Modular Annotated GUI Episodes)** is a framework for capturing, annotating, and visualizing web-based graphical user interfaces (GUIs). It is designed for researchers and developers working on GUI understanding, synthetic dataset generation, or automated interaction modeling.

## Features

- 📸 **Capture GUI**: Uses Playwright to take full-page screenshots and extract DOM element metadata.
- 🧠 **Annotate Elements**: Automatically labels and categorizes key interface components.
- 🖼️ **Visualize Episodes**: Builds visual episodes of the GUI, supporting different display modes (original, annotated, simplified).
- 📂 **Modular Design**: Each step is organized in its own script/module for easy customization and extension.

## Usage

First, install the required dependencies:

```bash
pip install -r requirements.txt
```
Then, run the main script:

```bash
python main.py
```
You can configure the target URL and visualization mode in `main.py`.

## Output

Each run generates a timestamped folder inside `/captures/`, which contains:

- `screenshot.png`: Full-page screenshot
- `elements.json`: Extracted and annotated DOM elements
- `annotated.png`: Image with overlaid annotations
- `episode.html`: Optional HTML visualization (if enabled)

## Dependencies

- Python 3.8+
- [Playwright](https://playwright.dev/python/)
- [Pillow](https://python-pillow.org/)
- Other standard libraries: `os`, `json`, `datetime`, etc.

## License

MIT License