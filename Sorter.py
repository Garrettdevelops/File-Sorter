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

if __name__ == "__main__":
    folder = input("Enter folder path to organize: ")
    organize_files(folder)
