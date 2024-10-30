import json
import tkinter as tk
from tkinter import ttk
import time
import win32api
import win32con
import win32gui

def print_open_windows():
    def enum_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            results.append((hwnd, title))

    results = []
    win32gui.EnumWindows(enum_callback, results)
    for hwnd, title in results:
        print(f"Window handle: {hwnd}, Title: {title}")


def downkey(window_handle):
    VK_DOWN = 0x28
    win32api.PostMessage(window_handle, win32con.WM_KEYDOWN, VK_DOWN, 0)
    win32api.PostMessage(window_handle, win32con.WM_KEYUP, VK_DOWN, 0)

def enterkey(window_handle):
    VK_RETURN = 0x0D
    win32api.PostMessage(window_handle, win32con.WM_KEYDOWN, VK_RETURN, 0)
    win32api.PostMessage(window_handle, win32con.WM_KEYUP, VK_RETURN, 0)



# Load movelist data from JSON file
def load_movelist_from_json():
    with open("movelist.json", "r") as file:
        movelist_data = json.load(file)
    return movelist_data

# GUI Application
class TekkenTrainerApp:
    def __init__(self, root, movelist_data, window_handle):
        self.root = root
        self.movelist_data = movelist_data
        self.window_handle = window_handle
        
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

    def send_commands(self, move_ids):
        if self.window_handle == 0:
            print(f"Window not found: {window_title}")
            return
        for move_id in move_ids:
            downkey(self.window_handle)
            time.sleep(0.05)
            enterkey(self.window_handle)
            time.sleep(0.05)
            downkey(self.window_handle)
            time.sleep(0.05)
            enterkey(self.window_handle)
            time.sleep(0.05)
            for _ in range(int(move_id) - 1):
                downkey(self.window_handle)
                time.sleep(0.05)
            enterkey(self.window_handle)
            time.sleep(0.05)
        
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
                
        self.send_commands(move_ids)            
        

if __name__ == "__main__":
     
    print_open_windows()
    window_title = "new 1 - Notepad++"
    window_handle = win32gui.FindWindow(None, window_title)
    print(f"Window handle: {window_handle}")   

    movelist_data = load_movelist_from_json()
    
    root = tk.Tk()
    app = TekkenTrainerApp(root, movelist_data, window_handle)
    root.mainloop()
