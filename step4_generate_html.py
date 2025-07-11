import json

def generate_html(elements, output_path):
    # Start HTML content
    html = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "  <meta charset='UTF-8'>",
        "  <title>GUI Navigation Training</title>",
        "  <style>",
        "    body { font-family: sans-serif; margin: 40px; }",
        "    .container { display: flex; flex-direction: column; gap: 10px; max-width: 600px; margin: auto; }",
        "    input, button, a { display: block; padding: 10px; font-size: 16px; }",
        "    a { text-decoration: none; color: blue; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <div class='container'>"
    ]

    # Create HTML elements from JSON
    for el in elements:
        el_type = el["type"]
        label = el["label"] or f"Unnamed {el_type.title()}"

        if el_type == "input":
            html.append(f"    <input type='text' placeholder='{label}' aria-label='{label}'>")
        elif el_type == "button":
            html.append(f"    <button>{label}</button>")
        elif el_type == "link":
            html.append(f"    <a href='#'>{label}</a>")

    # Close HTML
    html += [
        "  </div>",
        "</body>",
        "</html>"
    ]

    # Save to file
    with open(output_path, "w") as f:
        f.write("\n".join(html))

    print("HTML file 'mock_gui.html' has been created.")