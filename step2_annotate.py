import json
def annotate(elements):
    annotations = []
    
    # Element type to semantic label mapping
    TYPE_TO_LABEL = {
        "button": "button",
        "input": "text_field",
        "searchbox": "search_box",
        "link": "link",
        "dropdown": "dropdown",
        "checkbox": "checkbox",
        "radio": "radio_button"
    }
    
    for elem in elements:
        if not elem:
            continue
            
        # Convert Playwright bounding box to standard format [x_min, y_min, x_max, y_max]
        bbox = [
            elem["bbox"][0],  # x
            elem["bbox"][1],  # y
            elem["bbox"][0] + elem["bbox"][2],  # x + width
            elem["bbox"][1] + elem["bbox"][3]   # y + height
        ]
        
        # Determine semantic label
        element_type = elem.get("type", "unknown")
        label = TYPE_TO_LABEL.get(element_type, element_type)
        
        # Heuristic for actionability
        actionable = element_type in {
            "button", "link", "input", 
            "searchbox", "dropdown",
            "checkbox", "radio"
        }
        
        annotations.append({
            "bbox": bbox,
            "label": label,
            "element_type": element_type,
            "actionable": actionable,
            "text": elem.get("label", ""),
            "original_selector": elem.get("selector", "")
        })
    
    return annotations