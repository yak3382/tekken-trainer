import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Google Sheets setup
def setup_gspread_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "/home/yak/workspace/github.com/yak3382/t8_training_drills/private/aesthetic-fx-440001-a7-689d47a4444e.json", 
        scope
    )
    return gspread.authorize(creds)

# Fetch data from Google Sheets
def fetch_movelist_data(client):
    sheet = client.open("TekkenMovelist").worksheet("TekkenTrainerMovelist")
    rows = sheet.get_all_records()
    
    # Format data as JSON
    movelist_data = {}
    for row in rows:
        character = row["Character"]
        move_entry = {
            "ID": str(row["ID"]),  # Ensure ID is treated as a string
            "Move": str(row["Move"]),  # Ensure Move is treated as a string
            "Selectable": str(row["Selectable"])  # Ensure Selectable is treated as a string
        }
        
        # Add character's move list to dictionary
        if character not in movelist_data:
            movelist_data[character] = []
        movelist_data[character].append(move_entry)
    return movelist_data
    

# Save JSON data to a file
def save_json_file(data, filename="movelist.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

# Main function to run the conversion
if __name__ == "__main__":
    client = setup_gspread_client()
    movelist_data = fetch_movelist_data(client)
    save_json_file(movelist_data)
