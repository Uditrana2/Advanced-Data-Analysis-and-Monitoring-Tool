import re

# Function to categorize content based on keywords
def categorize_content(text):
    # Define keywords related to illegal topics
    illegal_keywords = ['drugs', 'cocaine', 'heroin', 'weapons', 'hacking', 'cc', 'cvv', 'credit card', 'bank account', 'passport']

    # Define keywords related to legal topics
    legal_keywords = ['marketplace', 'electronics', 'phone', 'computer', 'watch']

    # Check for illegal topics
    for keyword in illegal_keywords:
        if re.search(r'\b{}\b'.format(keyword), text, re.IGNORECASE):
            return "Illegal"

    # Check for legal topics
    for keyword in legal_keywords:
        if re.search(r'\b{}\b'.format(keyword), text, re.IGNORECASE):
            return "Legal"

    # Default category if no keywords found
    return "Uncategorized"

# Read the scraped data from the file
file_path = "sites705.txt"
try:
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
    exit()

# Split the data into sections (assuming each section is separated by <!DOCTYPE html>)
sections = re.split(r'<!DOCTYPE html>', data)

# Generate categorized headlines report
print("Categorized Headlines Report:")
print("=" * 30)
for i, section in enumerate(sections, start=1):
    category = categorize_content(section)
    print(f"Headline {i}: Category - {category}")
print("=" * 30)
