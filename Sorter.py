import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

CONFIG_FILE = "file_rules.json"

# Defines default categories and their file extensions
DEFAULT_EXTENSION_MAP = {
    'Images': ['.jpg', '.heic', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.docx', '.txt'],
    'Music': ['.mp3', '.wav'],
    '3D Printing': ['.3mf', '.obj', '.stl', '.amf', '.gcode'],
    'Disk Image Files': ['.dmg'],
    'ISO Files': ['.iso', '.raw', '.xz']
}

# Convert Category Map to Flat Extension
def flatten_extension_map(map_by_category):
    flat = {}
    for category, extensions in map_by_category.items():
        for ext in extensions:
            flat[ext.lower()] = category
    return flat

FLAT_EXTENSION_MAP = flatten_extension_map(DEFAULT_EXTENSION_MAP)

# Load and Save Config
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Config file is corrupted. Resetting to default.")
            return {ext: "" for ext in FLAT_EXTENSION_MAP.keys()}
    else:
        return {ext: "" for ext in FLAT_EXTENSION_MAP.keys()}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# Organize Files
def organize_files(source_folder, config, test_mode=False, recursive=False):
    if recursive:
        for root, dirs, files in os.walk(source_folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                _, ext = os.path.splitext(filename)
                ext = ext.lower()
                if ext in config and config[ext]:
                    dest_folder = config[ext]
                    os.makedirs(dest_folder, exist_ok=True)
                    dest_path = os.path.join(dest_folder, filename)
                    if test_mode:
                        print(f"[TEST] Would move: {file_path} → {dest_path}")
                    else:
                        shutil.move(file_path, dest_path)
    else:
        for filename in os.listdir(source_folder):
            file_path = os.path.join(source_folder, filename)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(filename)
                ext = ext.lower()
                if ext in config and config[ext]:
                    dest_folder = config[ext]
                    os.makedirs(dest_folder, exist_ok=True)
                    dest_path = os.path.join(dest_folder, filename)
                    if test_mode:
                        print(f"[TEST] Would move: {file_path} → {dest_path}")
                    else:
                        shutil.move(file_path, dest_path)

# GUI
class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom File Sorter")

        self.config = load_config()
        self.test_mode = tk.BooleanVar()

        self.build_gui()
        self.refresh_rule_list()

    def build_gui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        # Extension Rule List
        self.rule_list = tk.Listbox(frame, width=70)
        self.rule_list.grid(row=0, column=0, columnspan=3, pady=5)

        # Add/Update Rule
        tk.Label(frame, text="Extension:").grid(row=1, column=0)
        self.ext_entry = tk.Entry(frame)
        self.ext_entry.grid(row=1, column=1)
        tk.Button(frame, text="Set Folder", command=self.set_rule).grid(row=1, column=2)

        # Delete Rule
        tk.Button(frame, text="Delete Selected", command=self.delete_rule).grid(row=2, column=0, columnspan=3, pady=5)

        # Test Mode Checkbox
        tk.Checkbutton(frame, text="Test Mode (simulate only)", variable=self.test_mode).grid(row=3, column=0, columnspan=3)

        # Recursive file sort checkbox "include subfolders"
        self.recursive = tk.BooleanVar()
        tk.Checkbutton(frame, text="Include Subfolders", variable=self.recursive).grid(row=4, column=0, columnspan=3)

        # Run Button
        tk.Button(frame, text="Organize Folder", command=self.run_sorter).grid(row=5, column=0, columnspan=3, pady=10)

    def refresh_rule_list(self):
        self.rule_list.delete(0, tk.END)
        for ext, path in self.config.items():
            label = f"{ext:<6} → {path if path else '[Not Set]'}"
            self.rule_list.insert(tk.END, label)

    def set_rule(self):
        ext_input = self.ext_entry.get().strip().lower()
        extensions = [e.strip() if e.strip().startswith('.') else '.' + e.strip() for e in ext_input.split(',')]

        folder = filedialog.askdirectory()
        if folder:
            for ext in extensions:
                self.config[ext] = folder
            save_config(self.config)
            self.refresh_rule_list()
            self.ext_entry.delete(0, tk.END)

    def delete_rule(self):
        selection = self.rule_list.curselection()
        if selection:
            selected = self.rule_list.get(selection[0])
            ext = selected.split()[0]
            if ext in self.config:
                del self.config[ext]
                save_config(self.config)
                self.refresh_rule_list()

    def run_sorter(self):
        folder = filedialog.askdirectory(title="Select Folder to Organize")
        if folder:
            organize_files(folder, self.config, test_mode=self.test_mode.get(), recursive=self.recursive.get())
            if not self.test_mode.get():
                messagebox.showinfo("Done", "Files have been organized.")

if __name__ == '__main__':
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()

