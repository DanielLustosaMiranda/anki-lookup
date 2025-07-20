import csv
import requests
import os
import time

# --- Configuration ---
# The URL for the AnkiConnect API. Anki must be running for this to work.
ANKI_CONNECT_URL = "http://localhost:8765"

class AnkiDeckManager:
 
    def __init__(self, deck_name, csv_filename="ankicards_temp.csv"):
       
        self.deck_name = deck_name
        self.csv_filename = csv_filename
        self.anki_connect_url = ANKI_CONNECT_URL

    def _create_csv_file(self, cards):
       
        try:
            with open(self.csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Front', 'Back']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(cards)
            print(f"Successfully created '{self.csv_filename}' with {len(cards)} cards.")
            return True
        except IOError as e:
            print(f"Error: Could not write to file '{self.csv_filename}'. Reason: {e}")
            return False

    def _add_cards_from_csv(self):
       
        try:
            with open(self.csv_filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    payload = {
                        "action": "addNote",
                        "version": 6,
                        "params": {
                            "note": {
                                "deckName": self.deck_name,
                                "modelName": "Basic",
                                "fields": {
                                    "Front": row['Front'],
                                    "Back": row['Back']
                                },
                                "tags": ["automated-import", self.deck_name.replace(" ", "-")]
                            }
                        }
                    }
                    self._send_to_anki(payload, row['Front'])
        except FileNotFoundError:
            print(f"Error: The file '{self.csv_filename}' was not found.")
        except Exception as e:
            print(f"An unexpected error occurred during CSV processing: {e}")

    def _send_to_anki(self, payload, front_text):
       
        try:
            response = requests.post(self.anki_connect_url, json=payload).json()
            if response.get('error'):
                print(f"Anki Error: {response['error']}")
            else:
                print(f"Successfully added card: '{front_text[:40]}...'")
        except requests.exceptions.RequestException:
            print(f"\nError: Could not connect to AnkiConnect at {self.anki_connect_url}.")
            print("Please ensure Anki is running and the AnkiConnect add-on is installed.")
            # We return False to signal the process should stop
            return False
        return True

    def _delete_csv_file(self):
      
        try:
            os.remove(self.csv_filename)
            print(f"Successfully deleted temporary file: '{self.csv_filename}'")
        except FileNotFoundError:
            print(f"Info: File '{self.csv_filename}' was already deleted or never created.")
        except OSError as e:
            print(f"Error: Could not delete file '{self.csv_filename}'. Reason: {e}")

    def import_cards(self, cards_data):
            
        print(f"--- Starting Import for Deck: '{self.deck_name}' ---")
        
        # Step 1: Create the CSV file
        if not self._create_csv_file(cards_data):
            print("Aborting due to error creating CSV file.")
            return

        print("\n--- Adding Cards to Anki ---")
        time.sleep(1)
        
        # Step 2: Add cards from the CSV
        self._add_cards_from_csv()
        
        print("\n--- Cleaning Up ---")
        time.sleep(1)

        # Step 3: Delete the temporary file
        self._delete_csv_file()
        
        print("\n--- Process Complete ---")


# --- Main Execution Block ---
if __name__ == "__main__":
    # This block runs when the script is executed directly.
    
    # 1. Define the deck and the card data.
    deck = "Thermodynamics"
    cards = [
        {"Front": "State the First Law of Thermodynamics.", "Back": "Energy cannot be created or destroyed, only transferred or changed from one form to another. ΔU = Q - W"},
        {"Front": "What is an adiabatic process?", "Back": "A process that occurs without transferring heat or mass between a thermodynamic system and its surroundings."},
        {"Front": "Define Entropy (S).", "Back": "A measure of the amount of energy in a physical system that cannot be used to do work. It is a measure of the disorder or randomness of the system."},
        {"Front": "What is the Carnot Cycle?", "Back": "A theoretical thermodynamic cycle that gives the maximum possible efficiency that a heat engine can achieve during the conversion of heat into work."}
    ]
    
    # 2. Create an instance of the manager for the specified deck.
    deck_manager = AnkiDeckManager(deck_name=deck)
    
    # 3. Run the import process with the card data.
    deck_manager.import_cards(cards)

