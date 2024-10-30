import json
import tkinter as tk
from tkinter import ttk

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
            self.move_listbox.insert(tk.END, move)

# Run the App
if __name__ == "__main__":
    movelist_data = load_movelist_from_json()
    
    root = tk.Tk()
    app = TekkenTrainerApp(root, movelist_data)
    root.mainloop()
