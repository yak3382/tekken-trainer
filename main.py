import json
import tkinter as tk
from tkinter import ttk
import time
import pyautogui  # Make sure to install this library if you haven't yet

# Load movelist data from JSON file
def load_movelist_from_json():
    with open("movelist.json", "r") as file:
        movelist_data = json.load(file)
    return movelist_data

# GUI Application
class TekkenTrainerApp:
    def __init__(self, root, movelist_data):
        self.root = root
        self.movelist_data = movelist_data
        
        self.root.title("Tekken Trainer")
        self.root.geometry("400x400")
        
        # Character Dropdown
        self.character_var = tk.StringVar()
        self.character_label = tk.Label(root, text="Select Character:")
        self.character_label.pack()
        
        # Populate character dropdown with character names from JSON
        self.character_dropdown = ttk.Combobox(root, textvariable=self.character_var, state="readonly")
        self.character_dropdown['values'] = list(movelist_data.keys())
        self.character_dropdown.pack()
        
        # Move Listbox
        self.move_listbox = tk.Listbox(root, selectmode="multiple", height=10)
        self.move_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Load Moves Button
        self.load_moves_button = tk.Button(root, text="Load Moves", command=self.load_moves)
        self.load_moves_button.pack()

        # Execute Moves Button
        self.execute_moves_button = tk.Button(root, text="Execute Moves", command=self.execute_moves)
        self.execute_moves_button.pack()
        
    def load_moves(self):
        character_name = self.character_var.get()
        if not character_name:
            print("Select a character first!")
            return
        
        # Fetch moves for the selected character from JSON
        moves = self.movelist_data.get(character_name, [])
        
        # Update the Listbox
        self.move_listbox.delete(0, tk.END)
        for move in moves:
            move_name = move.get("Move")
            self.move_listbox.insert(tk.END, move_name)
        
    def execute_moves(self):
        selected_indices = self.move_listbox.curselection()
        selected_moves = [self.move_listbox.get(i) for i in selected_indices]
        
        if len(selected_moves) > 8:
            print("Please select a maximum of 8 moves.")
            return
        
        # Get IDs for selected moves
        move_ids = []
        for move in selected_moves:
            for character_moves in self.movelist_data.values():
                for move_info in character_moves:
                    if move_info["Move"] == move:
                        move_ids.append(move_info["ID"])
                        break
        
        # Execute the sequence of commands in the game
        self.send_commands(move_ids)

    def send_commands(self, move_ids):
        # Send input commands to Tekken 8
        pyautogui.press('s')  # First S to go down
        time.sleep(0.1)  # Small delay for the action to register
        pyautogui.press('j')  # Press J
        time.sleep(0.1)
        pyautogui.press('s')  # Second S to go down again
        time.sleep(0.1)
        pyautogui.press('j')  # Press J

        for move_id in move_ids:
            for _ in range(move_id - 1):  # Press S (ID - 1) times
                pyautogui.press('s')
                time.sleep(0.1)  # Small delay for the action to register
            pyautogui.press('j')  # Final J to select the move
            time.sleep(0.1)

if __name__ == "__main__":
    movelist_data = load_movelist_from_json()
    
    root = tk.Tk()
    app = TekkenTrainerApp(root, movelist_data)
    root.mainloop()
