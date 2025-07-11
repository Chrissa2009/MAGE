import os
import json
from datetime import datetime
from PIL import Image

from step1_capture_gui import capture_gui, save_capture
from step2_annotate import annotate
from step3_visualize import build_episode, plot_episode
from step4_generate_html import generate_html

# Load list of websites
URL = "https://www.instagram.com/"
MODE = "annotated"  # Change to "simplified" to show annotations only for actionable items

def main():
    print(f"Processing: {URL}")
    try:
        # === Step 1: Capture GUI ===
        elements, screenshot = capture_gui(URL)
        output_dir = save_capture(elements, screenshot)

        # === Step 2: Annotate Elements ===
        json_path = os.path.join(output_dir, "elements.json")
        with open(json_path, "r") as f:
            elements = json.load(f)
        annotations = annotate(elements)

        # === Step 3: Visualize ===
        image = Image.open(os.path.join(output_dir, "screenshot.png"))
        episode = build_episode(image, annotations)
        save_path = os.path.join(output_dir, f"{MODE}.png")
        plot_episode(episode, mode=MODE, save_path=save_path)

        # === Step 4: Convert to HTML ===
        html_path = os.path.join(output_dir, "mock_gui.html")
        generate_html(elements, output_path=html_path)

    except Exception as e:
        print(f"Failed to process {URL}: {e}")

if __name__ == "__main__":
    main()