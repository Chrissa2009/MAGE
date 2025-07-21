from bs4 import BeautifulSoup
import random, copy

def add_distractor(html, percentage_of_distraction):

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