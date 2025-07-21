from bs4 import BeautifulSoup
import random, copy

def add_distractor(html: str, percentage_of_distraction: float) -> str:

    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Define interactive element types to mutate
    interactive_selectors = ['button', 'input[type="submit"]', 'input[type="button"]', 'a[href]']

    # Sample distractor labels
    distractor_texts = ["Start", "Continue", "Not This", "Try Me", "Apply", "Go", "Cancel", "Maybe", "Nope", "Fake"]

    # Find all matching interactive elements
    targets = []
    for selector in interactive_selectors:
        targets += soup.select(selector)

    # Sample percentage of targets
    sampled_targets = random.sample(targets, int(len(targets) * percentage_of_distraction))

    for target in sampled_targets:
        # Clone the tag and its attributes
        clone = copy.copy(target)

        # Replace text or value depending on tag type
        new_label = random.choice(distractor_texts)

        if clone.name == "input" and clone.has_attr("value"):
            clone['value'] = new_label
        elif clone.name in ["button", "a", "textarea", "option"]:
            clone.string = new_label
        elif clone.has_attr("aria-label"):
            clone["aria-label"] = new_label
        else:
            clone.string = new_label

        # Random insert
        if random.random() > 0.5:
            target.insert_after(clone)
        else:
            target.insert_before(clone)
        
    return soup.prettify()

def shuffle_siblings(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    interactive_tags = {'button', 'a', 'input', 'select', 'textarea'}

    def is_interactive(tag):
        if not tag or not tag.name:
            return False
        if tag.name in interactive_tags:
            return True
        if tag.has_attr("onclick") or tag.has_attr("tabindex"):
            return True
        if tag.get("role") in {"button", "link", "checkbox", "radio"}:
            return True
        if tag.get("type") in {"button", "submit", "reset", "checkbox", "radio"}:
            return True
        return False

    for parent in soup.find_all():
        children = parent.find_all(recursive=False)

        interactive_children = [child for child in children if is_interactive(child)]
        if len(interactive_children) <= 1:
            continue

        # Retry until the shuffled order differs from original
        original_order = [str(child) for child in interactive_children]
        attempts = 0
        while True:
            random.shuffle(interactive_children)
            new_order = [str(child) for child in interactive_children]
            if new_order != original_order or attempts >= 50:
                break
            attempts += 1

        if new_order == original_order:
            continue  # Skip if failed to find a new order

        # Remove all interactive children from parent
        for child in interactive_children:
            child.extract()

        # Re-insert them at the same indices
        insert_positions = [i for i, c in enumerate(children) if is_interactive(c)]
        for i, idx in enumerate(insert_positions):
            # Insert after the element just before the target index
            if idx == 0:
                parent.insert(0, interactive_children[i])
            else:
                parent.insert(idx, interactive_children[i])

    return soup.prettify()