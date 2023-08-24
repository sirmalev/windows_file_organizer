import os
import tkinter as tk
from tkinter import filedialog

# The directory you want to organize
DIR_PATH = ''  # Example: 'C:/Users/YourName/Downloads'

# Mapping of file extensions to directory names
ORGANIZATION_MAP = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Videos': ['.mp4', '.mkv', '.flv', '.mpeg'],
    'Archives': ['.zip', '.tar', '.rar', '.gz'],
    'Other':['.exe','.lnk','.url',],
    # Add more categories as needed
}

# Extended organize_files function
def organize_files(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        

        # Skip if it's a directory
        if os.path.isdir(file_path):
            continue

        file_extension = os.path.splitext(filename)[1]
    
        for dir_name, extensions in ORGANIZATION_MAP.items():
            if file_extension in extensions:
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
    cat_var.set('')
    ext_var.set('')

def add_custom_category():
    cat_name = cat_var.get()
    exts = [e.strip() for e in ext_var.get().split(",")]
    for key in ORGANIZATION_MAP:
        if (cat_name.lower() == key.lower()):
            print(key)
            for val in exts:
                ORGANIZATION_MAP[key].append(val)
            dispose_entry()
            return        
    ORGANIZATION_MAP[cat_name] = exts
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

        for category, extensions in ORGANIZATION_MAP.items():
            tk.Button(new_window, text="Remove", command=lambda cat=category: remove_organize_folder(cat)).grid(row=row, column=0, sticky="w", padx=10, pady=5)

            tk.Label(new_window, text=category, font=("Arial", 12, "bold")).grid(row=row, column=1, sticky="w", padx=10, pady=5)
            column = 2
            for extension in extensions:
                # Create a variable to hold the checkbox state (0 for unchecked, 1 for checked)
                checkbox_state = tk.IntVar()
                checkbox_states[extension] = checkbox_state
                
                # Create a checkbox next to each extension
                tk.Checkbutton(new_window, variable=checkbox_state).grid(row=row, column=column)
                column += 1
                tk.Label(new_window, text=extension).grid(row=row, column=column, padx=5, pady=5)
                column += 1
            row += 1
        tk.Button(new_window, text="Remove Selected", command=update_map).grid(row=row+1, column=0, columnspan=10, pady=10)

    def remove_organize_folder(category):
        if category in ORGANIZATION_MAP:
            del ORGANIZATION_MAP[category]
        render_map()

    def update_map():
        for extension, state in checkbox_states.items():
            if state.get():
                for category, extensions in ORGANIZATION_MAP.items():
                    if extension in extensions:
                        extensions.remove(extension)  # Remove the extension from the category list

        # Remove categories with no extensions
        empty_categories = [category for category, extensions in ORGANIZATION_MAP.items() if not extensions]
        for category in empty_categories:
            del ORGANIZATION_MAP[category]
                        
        render_map()  # Refresh the window

    render_map()  # Initial rendering

# Main GUI setup
root = tk.Tk()
root.title("File Organizer")

dir_var = tk.StringVar()
result_var = tk.StringVar()
cat_var = tk.StringVar()
ext_var = tk.StringVar()


tk.Label(root, text="Directory Path:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=dir_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_directory).grid(row=0, column=2, padx=10, pady=10)
tk.Button(root, text="Organize Files", command=run_organizer).grid(row=1, column=0, columnspan=3, padx=10, pady=10)
tk.Label(root, textvariable=result_var,fg="green").grid(row=4, column=0, columnspan=9, padx=100, pady=10)
tk.Label(root, text="New Category:").grid(row=5, column=0)
tk.Entry(root, textvariable=cat_var,).grid(row=5, column=1)
tk.Label(root, text="Extensions (comma separated):").grid(row=6, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=ext_var).grid(row=6, column=1)
tk.Button(root, text="Add Category", command=add_custom_category).grid(row=5, column=2, rowspan=2, padx=10, pady=10)
tk.Button(root, text="Organization Map", command=open_new_window).grid(row=2, column=0, columnspan=3, padx=100, pady=10)
tk.Label(root, text="made by: sir.malev").grid(row=7, column=0, columnspan=3 ,padx=10, pady=10,)

root.mainloop()