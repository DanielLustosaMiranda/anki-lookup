import csv
import requests

def add_note(deck_name, front, back):
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": []
            }
        }
    }
    response = requests.post("http://localhost:8765", json=payload)
    return response.json()

with open('cards.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        front, back = row[0], row[1]
        print(add_note("Test", front, back))

# Usage
# From
print(add_note("Test", front, back))

# To (for example, a deck named "My Engineering Deck")
print(add_note("My Engineering Deck", front, back))
