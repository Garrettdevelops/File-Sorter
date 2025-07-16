import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

# Mapping extensions to folder names
EXTENSION_MAP = {
    'Images': ['.jpg', '.heic', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.docx', '.txt'],
    'Music': ['.mp3', '.wav'],
    '3d Printing': ['.3mf', '.OBJ', '.stl', '.amf', '.gcode'],
    'Disk Image Files': ['.dmg'],
    'ISO Files': ['.iso', '.raw', '.xz'],
}

def organize_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            ext = ext.lower()

            # Find the category for this file
            for folder, extensions in EXTENSION_MAP.items():
                if ext in extensions:
                    dest_folder = os.path.join(folder_path, folder)
                    os.makedirs(dest_folder, exist_ok=True)

                    shutil.move(file_path, os.path.join(dest_folder, filename))
                    print(f"Moved {filename} to {dest_folder}")
                    break

# GUI logic
def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        organize_files(folder)
        messagebox.showinfo("Done", "Files organized!")

# Build GUI
root = tk.Tk()
root.title("File Organizer")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Click below to select a folder to organize:")
label.pack(pady=5)

button = tk.Button(frame, text="Choose Folder", command=choose_folder)
button.pack(pady=10)

root.mainloop()
