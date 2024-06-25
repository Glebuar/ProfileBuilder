import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import json
from xml_processor import process_ixt_file

full_file_path = ""

def select_file():
    global full_file_path
    file_path = filedialog.askopenfilename(filetypes=[("IXT files", "*.ixt")])
    if file_path:
        if file_path.lower().endswith('.ixt'):
            full_file_path = file_path 
            display_path = truncate_path(file_path, max_length=55)
            file_label.config(text=display_path)
            create_profile_button.config(state=tk.NORMAL)
        else:
            file_label.config(text="Invalid file type")
            create_profile_button.config(state=tk.DISABLED)
    else:
        file_label.config(text="No file selected")
        create_profile_button.config(state=tk.DISABLED)

def save_profile():
    try:
        global full_file_path
        default_name = os.path.splitext(os.path.basename(full_file_path))[0] + ".json"
        file_path = filedialog.asksaveasfilename(defaultextension=".json", initialfile=default_name, filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            result, extracted_file = process_ixt_file(full_file_path)
            with open(file_path, 'w') as f:
                json.dump(result, f, indent=2)
            try:
                os.remove(extracted_file)
            except Exception:
                pass
            display_path = truncate_path(file_path, max_length=45)
            file_label.config(text=f"Saved to {display_path}")
            create_profile_button.config(state=tk.DISABLED)
        else:
            file_label.config(text="No file selected")
            create_profile_button.config(state=tk.DISABLED)
    except Exception as e:
        file_label.config(text=f"Error: {str(e)}")
        create_profile_button.config(state=tk.DISABLED)

def drop(event):
    global full_file_path
    file_path = event.data
    if file_path.lower().endswith('.ixt'):
        full_file_path = file_path 
        display_path = truncate_path(file_path, max_length=55)
        file_label.config(text=display_path)
        create_profile_button.config(state=tk.NORMAL)
    else:
        file_label.config(text="Invalid file type")
        create_profile_button.config(state=tk.DISABLED)

def truncate_path(path, max_length):
    if len(path) <= max_length:
        return path
    else:
        head, tail = os.path.split(path)
        truncated_head = f"...{head[-(max_length - len(tail) - 3):]}"
        return os.path.normpath(os.path.join(truncated_head, tail))

root = TkinterDnD.Tk()
root.title("Profile Builder - v1.0.0")
root.resizable(False, False)

frame = tk.Frame(root, width=400, height=200, bd=2, relief=tk.SUNKEN)
frame.pack(padx=10, pady=10)

upload_label = tk.Label(frame, text="  Drag and drop a file here or click the button to select a file  ")
upload_label.pack(pady=10)

file_label = tk.Label(frame, text="No file selected")
file_label.pack(pady=10)

select_button = tk.Button(frame, text="Select File", command=select_file)
select_button.pack(pady=10)

create_profile_button = tk.Button(frame, text="Create Profile", command=save_profile, state=tk.DISABLED)
create_profile_button.pack(pady=10)

frame.drop_target_register(DND_FILES)
frame.dnd_bind('<<Drop>>', drop)

root.mainloop()
