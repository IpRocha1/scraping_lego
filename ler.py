import json

# Load the JSON file
file_path = 'legos_lego_store_brasil.json'

with open(file_path, 'r', encoding="utf-8") as file:
    data = json.load(file)

# Get the number of items in the JSON file
num_items = len(data)
print(num_items)