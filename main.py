import os
import json
from datetime import datetime
from PIL import Image

from step1_capture_gui import capture_gui, save_capture
from step2_annotate import annotate
from step3_visualize import build_episode, plot_episode
URL = "https://onepagelove.com/page/2"
MODE = "annotated"  # Change to "simplified" if needed

def main():
    # === Step 1: Capture GUI ===
    elements, screenshot = capture_gui(URL)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join("captures", timestamp)
    save_capture(elements, screenshot)
    
    # === Step 2: Annotate Elements ===
    json_path = os.path.join(output_dir, "elements.json")
    with open(json_path, "r") as f:
        elements = json.load(f)
    annotations = annotate(elements)

    # === Step 3: Visualize ===
    image = Image.open(os.path.join(output_dir, "screenshot.png"))
    episode = build_episode(image, annotations)

    save_path = os.path.join(output_dir, f"{MODE}.png")
    plot_episode(episode, mode=MODE,save_path=save_path)

if __name__ == "__main__":
    main()