# 🧙 MAGE: Modular HTML Generation Engine

**MAGE** is a framework for generating realistic, diverse, and reusable HTML datasets. It is designed to support research and applications involving GUI navigation, visual grounding, or front-end testing by creating high-quality synthetic web data.

## 🔧 Project Modules

MAGE consists of three modular components:

### 1. **Template Generator**
Scrapes raw HTML pages using Playwright and extracts a reusable HTML structure with annotated placeholders.

- **Status**: ✅ Complete  
- **Run**:  
  ```bash
  python template_generator.py
  ```

### 2. **Mutator**

Takes base templates and programmatically generates diverse layout variants by modifying or duplicating components (e.g., buttons, links, containers).

- **Status**: 🔧 In progress

**Examples of mutations:**
- Duplicating action buttons  
- Adding/removing sections  
- Swapping layout elements

### 3. **Filler**

Populates template placeholders with realistic fake content using libraries like `Faker`, enabling dataset generation for training or UI testing.

- **Status**: 🔧 In progress

**Features:**
- Generates human-readable dummy content  
- Supports multiple field types (text, links, images)

## 📁 Project Structure
- **MAGE/**
  - `template_generator.py` - Scrapes and creates base HTML templates
  - `base_templates/` - Output templates with placeholders
  - `raw_html/` - Raw HTML snapshots
  - `clean_html/` - Cleaned HTML after processing
  - `screenshots/` - Screenshots of scraped pages
  - `mutator.py` - [WIP] Mutates base templates
  - `filler.py` - [WIP] Fills mutated templates with fake data

## 🛠️ Setup Instructions

### 1. Install Python dependencies:
```bash
pip install -r requirements.txt
playwright install
```

### 2. Run the template generator:
```bash
python template_generator.py
```

## 🚀 Use Cases

- GUI navigation research  
- Visual grounding datasets  
- Front-end testing automation  
- HTML layout benchmarking

## 📌 License

This project is released under the **MIT License © 2025 Chrissa da Gomez**.
