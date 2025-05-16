import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import string
import subprocess

# -----------------------------------------------------------------------------
# Build default_options list as a list of tuples: (description, underlying_value)
# -----------------------------------------------------------------------------
default_options = [("None", "0")]
default_options += [("MouseLeft", "1"), ("MouseMiddle", "2"),("MouseRight", "3")]
default_options += [("Pause Movement", "4"), ("Turbo Fire MouseLeft", "5"),("Turbo Fire/Reload MouseLeft/Right", "6")]
default_options += [("Border On/Off (Alt B)", "7")]
default_options += [("0", "8")]
default_options += [("1", "9")]
default_options += [("2", "10")]
default_options += [("3", "11")]
default_options += [("4", "12")]
default_options += [("5", "13")]
default_options += [("6", "14")]
default_options += [("7", "15")]
default_options += [("8", "16")]
default_options += [("9", "17")]
default_options += [(chr(i), str(i - 79)) for i in range(97, 123)] #lower case letters
default_options += [(chr(i), str(i - 21)) for i in range(65, 91)] #Upper Case letters
default_options += [("Return", "70")]
default_options += [("Space", "71")]
default_options += [("Escape", "72"),("Tab", "73"), ("Up", "74"), ("Down", "75"), ("Left", "76"), ("Right", "77")]
default_options += [("+", "78"),(",", "79"), ("-", "80"), (".", "81")]
default_options += [
    ("F1", "82"), ("F2", "83"), ("F3", "84"), ("F4", "85"), ("F5", "86"),
    ("F6", "87"), ("F7", "88"), ("F8", "89"), ("F9", "90"), ("F10", "91"),
    ("F11", "92"), ("F12", "93")
]

mod_options = [("None", "0"),("Shift", "1"),("Ctrl", "2"),("Alt", "3"),("WindowsKey", "4")]

# -----------------------------------------------------------------------------
# Check for the "SRS Configs" folder in the same directory and create it if it doesn't exist.
# -----------------------------------------------------------------------------
config_folder = "SRS Configs/Mappings"
if not os.path.exists(config_folder):
    os.mkdir(config_folder)

# -----------------------------------------------------------------------------
# Set config_options for each key.
# Every key uses the default_options list for its dropdown.
# -----------------------------------------------------------------------------
config_options = {
    "cbButtonTrigger":          {"label": "Trigger Button",             "options": default_options},
    "cbTriggerMod":             {"label": "Trigger Modifier",           "options": mod_options},
    "cbButtonTriggerOffscreen": {"label": "Trigger Button (Offscreen)", "options": default_options},
    "cbTriggerModOffscreen":    {"label": "Trigger Modifier (Offscreen)", "options": default_options},

    "cbButtonPumpAction":          {"label": "Pump Action Button",         "options": default_options},
    "cbPumpActionMod":             {"label": "Pump Action Modifier",       "options": default_options},
    "cbButtonPumpActionOffscreen": {"label": "Pump Action Button (Offscreen)", "options": default_options},
    "cbPumpActionModOffscreen":    {"label": "Pump Action Modifier (Offscreen)", "options": default_options},

    "cbButtonFrontLeft":         {"label": "Front Left Button",         "options": default_options},
    "cbFrontLeftMod":            {"label": "Front Left Modifier",       "options": default_options},
    "cbButtonFrontLeftOffscreen": {"label": "Front Left Button (Offscreen)", "options": default_options},
    "cbFrontLeftModOffscreen":    {"label": "Front Left Modifier (Offscreen)", "options": default_options},

    "cbButtonRearLeft":          {"label": "Rear Left Button",          "options": default_options},
    "cbRearLeftMod":             {"label": "Rear Left Modifier",        "options": default_options},
    "cbButtonRearLeftOffscreen": {"label": "Rear Left Button (Offscreen)", "options": default_options},
    "cbRearLeftModOffscreen":    {"label": "Rear Left Modifier (Offscreen)", "options": default_options},

    "cbButtonFrontRight":         {"label": "Front Right Button",        "options": default_options},
    "cbFrontRightMod":            {"label": "Front Right Modifier",      "options": default_options},
    "cbButtonFrontRightOffscreen": {"label": "Front Right Button (Offscreen)", "options": default_options},
    "cbFrontRightModOffscreen":    {"label": "Front Right Modifier (Offscreen)", "options": default_options},

    "cbButtonRearRight":         {"label": "Rear Right Button",         "options": default_options},
    "cbRearRightMod":            {"label": "Rear Right Modifier",       "options": default_options},
    "cbButtonRearRightOffscreen": {"label": "Rear Right Button (Offscreen)", "options": default_options},
    "cbRearRightModOffscreen":    {"label": "Rear Right Modifier (Offscreen)", "options": default_options},

    "cbButtonUp":         {"label": "Up Button",         "options": default_options},
    "cbUpMod":            {"label": "Up Modifier",       "options": default_options},
    "cbButtonUpOffscreen": {"label": "Up Button (Offscreen)", "options": default_options},
    "cbUpModOffscreen":    {"label": "Up Modifier (Offscreen)", "options": default_options},

    "cbButtonDown":         {"label": "Down Button",         "options": default_options},
    "cbDownMod":            {"label": "Down Modifier",       "options": default_options},
    "cbButtonDownOffscreen": {"label": "Down Button (Offscreen)", "options": default_options},
    "cbDownModOffscreen":    {"label": "Down Modifier (Offscreen)", "options": default_options},

    "cbButtonLeft":         {"label": "Left Button",         "options": default_options},
    "cbLeftMod":            {"label": "Left Modifier",       "options": default_options},
    "cbButtonLeftOffscreen": {"label": "Left Button (Offscreen)", "options": default_options},
    "cbLeftModOffscreen":    {"label": "Left Modifier (Offscreen)", "options": default_options},

    "cbButtonRight":         {"label": "Right Button",         "options": default_options},
    "cbRightMod":            {"label": "Right Modifier",       "options": default_options},
    "cbButtonRightOffscreen": {"label": "Right Button (Offscreen)", "options": default_options},
    "cbRightModOffscreen":    {"label": "Right Modifier (Offscreen)", "options": default_options},
    
    # -----------------------------------------------------------------------------
    # New primary key: Pedal button (no modifier or offscreen option needed)
    # -----------------------------------------------------------------------------
    "cbButtonPedal": {"label": "Pedal Button", "options": default_options}
}

# -----------------------------------------------------------------------------
# Define groups for arranging keys.
# Each group (except for the newly added pedal) is a list of 4 keys in the order:
# [Primary Button, Primary Modifier, Offscreen Button, Offscreen Modifier]
# -----------------------------------------------------------------------------
groups = [
    ["cbButtonTrigger", "cbTriggerMod", "cbButtonTriggerOffscreen", "cbTriggerModOffscreen"],
    ["cbButtonPumpAction", "cbPumpActionMod", "cbButtonPumpActionOffscreen", "cbPumpActionModOffscreen"],
    ["cbButtonFrontLeft", "cbFrontLeftMod", "cbButtonFrontLeftOffscreen", "cbFrontLeftModOffscreen"],
    ["cbButtonRearLeft", "cbRearLeftMod", "cbButtonRearLeftOffcreen", "cbRearLeftModOffscreen"],
    ["cbButtonFrontRight", "cbFrontRightMod", "cbButtonFrontRightOffscreen", "cbFrontRightModOffscreen"],
    ["cbButtonRearRight", "cbRearRightMod", "cbButtonRearRightOffscreen", "cbRearRightModOffscreen"],
    ["cbButtonUp", "cbUpMod", "cbButtonUpOffscreen", "cbUpModOffscreen"],
    ["cbButtonDown", "cbDownMod", "cbButtonDownOffscreen", "cbDownModOffscreen"],
    ["cbButtonLeft", "cbLeftMod", "cbButtonLeftOffscreen", "cbLeftModOffscreen"],
    ["cbButtonRight", "cbRightMod", "cbButtonRightOffscreen", "cbRightModOffscreen"]
]

# -----------------------------------------------------------------------------
# Add the pedal key as its own group (it will occupy an entire row by itself)
# -----------------------------------------------------------------------------
groups.append(["cbButtonPedal"])

# Create a flat list of all keys (for file operations).
keys_to_replace = sum(groups, [])

# -----------------------------------------------------------------------------
# Global dictionaries to hold:
# - The StringVar for each key's OptionMenu.
# - Dropdown mappings for each key: description -> underlying value and vice versa.
# -----------------------------------------------------------------------------
dropdowns = {}
dropdown_mappings = {}

global file_path
file_path = ""


# -----------------------------------------------------------------------------
# File Operations Functions
# -----------------------------------------------------------------------------
def update_file():
    file_path = filedialog.askopenfilename(
        title="Select Configuration File",
        initialfile = "Lightgun.exe.config",
        initialdir= os.path.dirname(os.path.abspath(__file__)),
        filetypes=[("Config Files", "*.config"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    with open(file_path, "r") as file:
        lines = file.readlines()

    # Update lines that match a key's pattern.
    for i, line in enumerate(lines):
        for key in keys_to_replace:
            if line.strip().startswith(f'<add key="{key}" value'):
                # Retrieve the selected description from the dropdown.
                desc = dropdowns[key].get()
                # Look up the underlying value.
                underlying_value = dropdown_mappings[key]["desc_to_val"].get(desc, desc)
                lines[i] = re.sub(r'value="[^"]*"', f'value="{underlying_value}"', line)

    with open(file_path, "w") as file:
        file.writelines(lines)
    messagebox.showinfo("Success", "File updated successfully!")
    
def export_values():
    file_path = filedialog.asksaveasfilename(
        title="Save Configuration",
        initialdir=config_folder,
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    try:
        with open(file_path, "w") as file:
            for key in keys_to_replace:
                desc = dropdowns[key].get()
                underlying_value = dropdown_mappings[key]["desc_to_val"].get(desc, desc)
                file.write(f"{key},{underlying_value}\n")
        messagebox.showinfo("Success", "Configuration exported successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export configuration:\n{e}")

def import_values():
    file_path = filedialog.askopenfilename(
        title="Select Configuration File",
        initialdir=config_folder,
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    
    if not file_path:
        return

    file_label.config(text=f"Imported file: " +os.path.basename(file_path), font=("Arial", 12))
    
    try:
        with open(file_path, "r") as file:
            for line in file:
                try:
                    key, value = line.strip().split(",", 1)
                    if key in dropdown_mappings:
                        desc = dropdown_mappings[key]["val_to_desc"].get(value, value)
                        dropdowns[key].set(desc)
                except ValueError:
                    continue
        messagebox.showinfo("Success", "Configuration imported successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to import configuration:\n{e}")


def run_sinden():
    currentpath = os.path.dirname(os.path.abspath(__file__))
    Sindenfilepath = os.path.join(currentpath, "lightgun.exe") 

    try:
        result = subprocess.run([Sindenfilepath], check=True, capture_output=True, text=True)
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)


# -----------------------------------------------------------------------------
# Build the UI.
# -----------------------------------------------------------------------------
root = tk.Tk()
root.title("Sinden Remapper Software (SRS)")

# Create a Notebook widget
notebook = ttk.Notebook(root)

# Create frames for each tab
tab1 = ttk.Frame(notebook)


# Add tabs to the Notebook
notebook.add(tab1, text="Mapping")


# Top frame for the operation buttons.
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
file_name = file_path
#file_label = ttk.Label(tab1, text=f"Imported file:" + file_name, font=("Arial", 12)).grid(row=1, column=3, padx=5)
file_label = tk.Label(root, text="No file imported yet")
file_label.pack()

ttk.Button(tab1, text="Import Config", command=import_values).grid(row=0, column=0, padx=5)
ttk.Button(tab1, text="Export Config", command=export_values).grid(row=0, column=1, padx=5)
ttk.Button(tab1, text="Push to Sinden Settings", command=update_file).grid(row=0, column=2, padx=5)

tk.Button(button_frame, text="Start Sinden", command=run_sinden).grid(row=0, column=3, padx=5)



# Frame for the grid-based layout.
frame = ttk.Frame(root)
frame.pack(pady=10)
row_offset = 2
# For each group, create one row with each key's label and dropdown.
for group_index, group in enumerate(groups):
    for col_index, key in enumerate(group):
        label_col = col_index * 2         # Label in one column.
        dropdown_col = col_index * 2 + 1    # Dropdown in the next column.
        
        label_text = config_options.get(key, {}).get("label", key)
        ttk.Label(tab1, text=label_text, anchor="w").grid(
            row=group_index + row_offset, column=label_col, sticky="w", padx=5, pady=5
        )
        
        # Retrieve the options (tuples) for this key.
        options = config_options.get(key, {}).get("options", default_options)
        if not options or not isinstance(options[0], tuple):
            options = [(opt, opt) for opt in options]
        
        # Build mapping dictionaries: description → value and vice versa.
        desc_to_val = {desc: val for desc, val in options}
        val_to_desc = {val: desc for desc, val in options}
        dropdown_mappings[key] = {"desc_to_val": desc_to_val, "val_to_desc": val_to_desc}
        
        var = tk.StringVar(value=options[0][0])
        dropdown = ttk.OptionMenu(tab1, var, *[desc for desc, val in options])
        dropdown.grid(row=group_index + row_offset, column=dropdown_col, padx=5, pady=2)
        dropdowns[key] = var

notebook.pack(expand=True, fill='both')

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Recoil")

def on_click(event):
    # Get the line number where the user clicked
    index = text.index(ttk.CURRENT)
    line = index.split('.')[0]
    
    # Retrieve the file name from the clicked line
    file_name = text.get(f"{line}.0", f"{line}.end").strip()
    print(f"Clicked on: {file_name}")  # Replace with desired action
    
    
def list_files(folder_path):
    folder_path = "SRS Configs/Recoil"
    files = os.listdir(folder_path)
    text.delete("1.0", tk.END)  # Clear previous entries
    for file in files:
        text.insert(tk.END, file + "\n")  # Add files to the Text widget
#ttk.Button(tab2, text="Push to Sinden Settings", command=update_file).grid(row=0, column=2, padx=5)
# Create a Text widget
text = tk.Text(tab2, wrap="none", height=15, width=50)
text.pack()

# Add a button to tab2
button = ttk.Button(tab2, text="Export to Sinden", command=lambda: list_files(folder_path))
button.pack(pady=5)


# Bind click event
text.bind("<Button-1>", on_click)

# Specify the folder path (change this to the desired folder)
folder_path = "./"  # Current directory
list_files(folder_path)


# Pack the Notebook widget
notebook.pack(expand=True, fill="both")

root.mainloop()
