import subprocess
import os, shutil

print("Step 1: Scraping pages...")
subprocess.run(["python", "scrape_pages.py"])

print("Step 2: Cleaning HTML...")
subprocess.run(["python", "clean_html.py"])

print("Step 3: Validating via screenshots...")
subprocess.run(["python", "validate_html.py"])

# Step 4: Organize into base_template folder
print("Step 4: Moving into base_template folder...")
os.makedirs("base_template", exist_ok=True)

for folder in ["raw_html", "clean_html", "screenshots"]:
    if os.path.exists(folder):
        shutil.move(folder, f"base_template/{folder}")

print("Pipeline completed. Files saved in 'base_template/'")