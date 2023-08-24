import os
import tkinter as tk
from tkinter import filedialog

# Copyright (C) 2023 sir.malev
# 
# All rights reserved.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# The directory you want to organize
DIR_PATH = ''  

# Mapping of file types to directory names
ORGANIZATION_MAP = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Videos': ['.mp4', '.mkv', '.flv', '.mpeg'],
    'Archives': ['.zip', '.tar', '.rar', '.gz'],
    'Other':['.exe','.lnk','.url',],
}

# Extended organize_files function
def organize_files(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        

        # Skip if it's a directory
        if os.path.isdir(file_path):
            continue

        file_type = os.path.splitext(filename)[1]
    
        for dir_name, types in ORGANIZATION_MAP.items():
            if file_type in types:
                # Create directory if it doesn't exist
                new_dir_path = os.path.join(dir_path, dir_name)
                if not os.path.exists(new_dir_path):
                    os.mkdir(new_dir_path)
                
                # Move the file
                os.rename(file_path, os.path.join(new_dir_path, filename))
                break


def select_directory():
    folder_selected = filedialog.askdirectory()
    dir_var.set(folder_selected)

def run_organizer():
    organize_files(dir_var.get())
    result_var.set("Files organized!")

def dispose_entry():
    fold_var.set('')
    type_var.set('')

def add_custom_folder():
    fold_name = fold_var.get()
    exts = [e.strip() for e in type_var.get().split(",")]
    for key in ORGANIZATION_MAP:
        if (fold_name.lower() == key.lower()):
            print(key)
            for val in exts:
                ORGANIZATION_MAP[key].append(val)
            dispose_entry()
            return        
    ORGANIZATION_MAP[fold_name] = exts
    dispose_entry()


# Load custom map at the beginning

def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("Organization Map")
    checkbox_states = {}  # Dictionary to track the states of each checkbox

    def render_map():
        row = 0
        for widget in new_window.winfo_children():
            widget.destroy()  # Clear the window

        for folder, types in ORGANIZATION_MAP.items():
            tk.Button(new_window, text="Remove", command=lambda fold=folder: remove_organize_folder(fold)).grid(row=row, column=0, sticky="w", padx=10, pady=5)

            tk.Label(new_window, text=folder, font=("Arial", 12, "bold")).grid(row=row, column=1, sticky="w", padx=10, pady=5)
            column = 2
            for type in types:
                # Create a variable to hold the checkbox state (0 for unchecked, 1 for checked)
                checkbox_state = tk.IntVar()
                checkbox_states[type] = checkbox_state
                
                # Create a checkbox next to each file type
                tk.Checkbutton(new_window, variable=checkbox_state).grid(row=row, column=column)
                column += 1
                tk.Label(new_window, text=type).grid(row=row, column=column, padx=5, pady=5)
                column += 1
            row += 1
        tk.Button(new_window, text="Remove Selected", command=update_map).grid(row=row+1, column=0, columnspan=10, pady=10)

    def remove_organize_folder(folder):
        if folder in ORGANIZATION_MAP:
            del ORGANIZATION_MAP[folder]
        render_map()

    def update_map():
        for type, state in checkbox_states.items():
            if state.get():
                for folder, types in ORGANIZATION_MAP.items():
                    if type in types:
                        types.remove(type)  # Remove the file type from the folder list

        # Remove folders with no file types
        empty_folders = [folder for folder, types in ORGANIZATION_MAP.items() if not types]
        for folder in empty_folders:
            del ORGANIZATION_MAP[folder]
                        
        render_map()  # Refresh the window

    render_map()  # Initial rendering

# Main GUI setup
root = tk.Tk()
root.title("File Organizer")

dir_var = tk.StringVar()
result_var = tk.StringVar()
fold_var = tk.StringVar()
type_var = tk.StringVar()


tk.Label(root, text="Directory Path:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=dir_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_directory).grid(row=0, column=2, padx=10, pady=10)
tk.Button(root, text="Organize Files", command=run_organizer).grid(row=1, column=0, columnspan=3, padx=10, pady=10)
tk.Label(root, textvariable=result_var,fg="green").grid(row=4, column=0, columnspan=9, padx=100, pady=10)
tk.Label(root, text="New Folder:").grid(row=5, column=0)
tk.Entry(root, textvariable=fold_var,).grid(row=5, column=1)
tk.Label(root, text="Type of File (comma separated):").grid(row=6, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=type_var).grid(row=6, column=1)
tk.Button(root, text="Add Type", command=add_custom_folder).grid(row=5, column=2, rowspan=2, padx=10, pady=10)
tk.Button(root, text="Organization Map", command=open_new_window).grid(row=2, column=0, columnspan=3, padx=100, pady=10)
tk.Label(root, text="made by: sir.malev").grid(row=7, column=0, columnspan=3 ,padx=10, pady=10,)

root.mainloop()