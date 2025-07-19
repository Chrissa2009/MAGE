import asyncio
from step1_create_templates import fetch_html, create_template, mutate_template
from step2_fill_template import fill_template, save_html

async def main():
    # Step 1: Scrape google.com
    original_html = await fetch_html()

    # Step 2: Create a base template with placeholders
    base_template = create_template(original_html)
    save_html(base_template, 'template_base.html')

    # Step 3: Mutate the template by duplicating buttons
    mutated_templates = mutate_template(base_template, num_variants=3)

    for i, mutated_html in enumerate(mutated_templates):
        filename_template = f'mutated_template_{i+1}.html'
        filename_generated = f'generated_mutated_{i+1}.html'

        # Save the raw mutated template
        save_html(mutated_html, filename_template)

        # Optional: fill out placeholders if needed
        replacements = {
            'link1': 'https://example.com',
            'text1': 'Example Link',
            'link2': 'https://chat.openai.com',
            'text2': 'ChatGPT',
            'link3': 'https://news.ycombinator.com',
            'text3': 'Hacker News'
        }

        final_html = fill_template(mutated_html, replacements)
        save_html(final_html, filename_generated)

if __name__ == '__main__':
    asyncio.run(main())