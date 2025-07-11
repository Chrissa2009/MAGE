import matplotlib.pyplot as plt
from PIL import ImageDraw
from PIL import Image

def build_episode(original_image, annotations):
    episode = {
        "image": original_image,
        "annotations": annotations
    }
    return episode

def plot_episode(episode, mode, save_path):
    """
    Display a website screenshot in one of three modes:
    - 'original': raw screenshot only
    - 'annotated': draw all elements as bounding boxes with labels
    """
    img = episode["image"].copy()
    draw = ImageDraw.Draw(img)

    if mode == "annotated":
        for ann in episode["annotations"]:
            x0, y0, x1, y1 = ann["bbox"]
            label = ann.get("label", "")
            draw.rectangle([x0, y0, x1, y1], outline="red", width=2)
            draw.text((x0, y0 - 10), label, fill="red")

    elif mode == "simplified":
        for ann in episode["annotations"]:
            if ann.get("actionable"):
                x0, y0, x1, y1 = ann["bbox"]
                draw.rectangle([x0, y0, x1, y1], outline="blue", width=2)
    
    if save_path:
        img.save(save_path)
        print(f"Saved annotated image to {save_path}")

    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    plt.axis("off")
    plt.show()