import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import string
import subprocess
import shutil
import platform
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
    "cbTriggerModOffscreen":    {"label": "Trigger Modifier (Offscreen)", "options": mod_options},

    "cbButtonPumpAction":          {"label": "Pump Action Button",         "options": default_options},
    "cbPumpActionMod":             {"label": "Pump Action Modifier",       "options": mod_options},
    "cbButtonPumpActionOffscreen": {"label": "Pump Action Button (Offscreen)", "options": default_options},
    "cbPumpActionModOffscreen":    {"label": "Pump Action Modifier (Offscreen)", "options": mod_options},

    "cbButtonFrontLeft":         {"label": "Front Left Button",         "options": default_options},
    "cbFrontLeftMod":            {"label": "Front Left Modifier",       "options": mod_options},
    "cbButtonFrontLeftOffscreen": {"label": "Front Left Button (Offscreen)", "options": default_options},
    "cbFrontLeftModOffscreen":    {"label": "Front Left Modifier (Offscreen)", "options": mod_options},

    "cbButtonRearLeft":          {"label": "Rear Left Button",          "options": default_options},
    "cbRearLeftMod":             {"label": "Rear Left Modifier",        "options": mod_options},
    "cbButtonRearLeftOffscreen": {"label": "Rear Left Button (Offscreen)", "options": default_options},
    "cbRearLeftModOffscreen":    {"label": "Rear Left Modifier (Offscreen)", "options": mod_options},

    "cbButtonFrontRight":         {"label": "Front Right Button",        "options": default_options},
    "cbFrontRightMod":            {"label": "Front Right Modifier",      "options": mod_options},
    "cbButtonFrontRightOffscreen": {"label": "Front Right Button (Offscreen)", "options": default_options},
    "cbFrontRightModOffscreen":    {"label": "Front Right Modifier (Offscreen)", "options": mod_options},

    "cbButtonRearRight":         {"label": "Rear Right Button",         "options": default_options},
    "cbRearRightMod":            {"label": "Rear Right Modifier",       "options": mod_options},
    "cbButtonRearRightOffscreen": {"label": "Rear Right Button (Offscreen)", "options": default_options},
    "cbRearRightModOffscreen":    {"label": "Rear Right Modifier (Offscreen)", "options": mod_options},

    "cbButtonUp":         {"label": "Up Button",         "options": default_options},
    "cbUpMod":            {"label": "Up Modifier",       "options": mod_options},
    "cbButtonUpOffscreen": {"label": "Up Button (Offscreen)", "options": default_options},
    "cbUpModOffscreen":    {"label": "Up Modifier (Offscreen)", "options": mod_options},

    "cbButtonDown":         {"label": "Down Button",         "options": default_options},
    "cbDownMod":            {"label": "Down Modifier",       "options": mod_options},
    "cbButtonDownOffscreen": {"label": "Down Button (Offscreen)", "options": default_options},
    "cbDownModOffscreen":    {"label": "Down Modifier (Offscreen)", "options": mod_options},

    "cbButtonLeft":         {"label": "Left Button",         "options": default_options},
    "cbLeftMod":            {"label": "Left Modifier",       "options": mod_options},
    "cbButtonLeftOffscreen": {"label": "Left Button (Offscreen)", "options": default_options},
    "cbLeftModOffscreen":    {"label": "Left Modifier (Offscreen)", "options": mod_options},

    "cbButtonRight":         {"label": "Right Button",         "options": default_options},
    "cbRightMod":            {"label": "Right Modifier",       "options": mod_options},
    "cbButtonRightOffscreen": {"label": "Right Button (Offscreen)", "options": default_options},
    "cbRightModOffscreen":    {"label": "Right Modifier (Offscreen)", "options": mod_options},
    
    # -----------------------------------------------------------------------------
    # New primary key: Pedal button (no modifier or offscreen option needed)
    # -----------------------------------------------------------------------------
    "cbButtonPedal": {"label": "Pedal Button", "options": default_options},
    "chkEnableJoystick": {"label": "Joystick Enabled", "options": default_options},
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
    ["cbButtonRearLeft", "cbRearLeftMod", "cbButtonRearLeftOffscreen", "cbRearLeftModOffscreen"],
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
    current_path = os.path.dirname(os.path.abspath(__file__))
    sinden_filepath = os.path.join(current_path, "lightgun.exe")
    try:
        result = subprocess.run(
            [sinden_filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("Success:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
    except Exception as e:
        print("An exception occurred:", str(e))



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
#NEW

folder_path = "SRS Configs/Recoil"
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

def on_click(event):
    """
    Get the line in the Text widget where the user clicked and print the file name.
    """
    # Use "current" index (works with grid; ttk.CURRENT may not work with Text widget)
    index = text.index("current")
    line = index.split('.')[0]
    file_name = text.get(f"{line}.0", f"{line}.end").strip()
    print(f"Clicked on: {file_name}")
    recoilimport_values()

def list_files(dummy_folder_path):
    """
    List files from the hard-coded folder "SRS Configs/Recoil" and insert them into the Text widget.
    (The input parameter is ignored in this example.)
    """
    folder_path = "SRS Configs/Recoil"
    try:
        files = os.listdir(folder_path)
    except Exception as e:
        files = [f"Error: {e}"]
    text.delete("1.0", tk.END)
    for file in files:
        text.insert(tk.END, file + "\n")

def recoilexport_values():
    """
    Gather recoil settings from various controls,
    export them in a human-readable text file, and display a message confirming the export.
    """
    settings = {
        "chkRecoilTerms": var_chkRecoilTerms.get(),
        "chkEnableRecoil": var_chkEnableRecoil.get(),
        "chkRecoilTrigger": var_chkRecoilTrigger.get(),
        "chkRecoilTriggerOffscreen": var_chkRecoilTriggerOffscreen.get(),
        "chkRecoilPumpActionOnEvent": var_chkRecoilPumpActionOnEvent.get(),
        "chkRecoilPumpActionOffEvent": var_chkRecoilPumpActionOffEvent.get(),
        "chkRecoilFrontLeft": var_chkRecoilFrontLeft.get(),
        "chkRecoilFrontRight": var_chkRecoilFrontRight.get(),
        "chkRecoilBackLeft": var_chkRecoilBackLeft.get(),
        "chkRecoilBackRight": var_chkRecoilBackRight.get(),
        "chkRecoilAlternative": var_chkRecoilAlternative.get(),
        "trkRecoilStrength": var_trkRecoilStrength.get(),
        "radTriggerRecoil": var_radTriggerRecoil.get(),  # 1 for Normal; 0 for Repeat
        "trkRecoilSlider": var_trkRecoilSlider.get(),
        "trkStartDelay": var_trkStartDelay.get(),
        "trkDelayBetweenPulses": var_trkDelayBetweenPulses.get(),
    }
 
    # Open a file dialog for the user to select where to save the exported file
    file_path = filedialog.asksaveasfilename(
        title="Export Recoil Configuration",
        defaultextension=".txt",
        initialdir="SRS Configs/Recoil",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    # Exit if the user cancelled the operation
    if not file_path:
        return

    try:
        with open(file_path, "w") as f:
            f.write("Recoil Configuration Values\n")
            f.write("-----------------------------\n")
            for key, value in settings.items():
                f.write(f"{key}: {value}\n")
        messagebox.showinfo("Export", "Recoil configuration values exported!")
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred during export:\n{e}")
    list_files(dummy_folder_path)
def recoilimport_values():
    """
    Open a recoil configuration text file, parse the settings, and update the
    corresponding control variables.
    """
    # Open a file dialog for the user to select the file to import
    file_path = filedialog.askopenfilename(
        title="Import Recoil Configuration",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    # Exit if the user cancels
    if not file_path:
        return

    try:
        with open(file_path, "r") as f:
            # Read all lines from the file
            lines = f.readlines()

        # Assuming the first two lines are header lines, we skip them.
        # The rest of the file should contain lines "key: value"
        config = {}
        for line in lines[2:]:
            # Remove surrounding whitespace and newlines
            line = line.strip()
            if not line:
                continue
            if ": " in line:
                key, value = line.split(": ", 1)
                config[key.strip()] = value.strip()

        # Try to parse values to the proper types
        parsed_config = {}
        for key, value in config.items():
            # Convert string booleans to actual booleans if applicable
            if value.lower() == "true":
                parsed_config[key] = True
            elif value.lower() == "false":
                parsed_config[key] = False
            else:
                # Attempt to convert to int
                try:
                    parsed_config[key] = int(value)
                except ValueError:
                    # If int fails, try float conversion
                    try:
                        parsed_config[key] = float(value)
                    except ValueError:
                        # Otherwise, keep it as string
                        parsed_config[key] = value

        # Update application variables with the imported settings.
        # Ensure that these Tkinter variables exist in your scope.
        if "chkRecoilTerms" in parsed_config:
            var_chkRecoilTerms.set(parsed_config["chkRecoilTerms"])
        if "chkEnableRecoil" in parsed_config:
            var_chkEnableRecoil.set(parsed_config["chkEnableRecoil"])
        if "chkRecoilTrigger" in parsed_config:
            var_chkRecoilTrigger.set(parsed_config["chkRecoilTrigger"])
        if "chkRecoilTriggerOffscreen" in parsed_config:
            var_chkRecoilTriggerOffscreen.set(parsed_config["chkRecoilTriggerOffscreen"])
        if "chkRecoilPumpActionOnEvent" in parsed_config:
            var_chkRecoilPumpActionOnEvent.set(parsed_config["chkRecoilPumpActionOnEvent"])
        if "chkRecoilPumpActionOffEvent" in parsed_config:
            var_chkRecoilPumpActionOffEvent.set(parsed_config["chkRecoilPumpActionOffEvent"])
        if "chkRecoilFrontLeft" in parsed_config:
            var_chkRecoilFrontLeft.set(parsed_config["chkRecoilFrontLeft"])
        if "chkRecoilFrontRight" in parsed_config:
            var_chkRecoilFrontRight.set(parsed_config["chkRecoilFrontRight"])
        if "chkRecoilBackLeft" in parsed_config:
            var_chkRecoilBackLeft.set(parsed_config["chkRecoilBackLeft"])
        if "chkRecoilBackRight" in parsed_config:
            var_chkRecoilBackRight.set(parsed_config["chkRecoilBackRight"])
        if "chkRecoilAlternative" in parsed_config:
            var_chkRecoilAlternative.set(parsed_config["chkRecoilAlternative"])
        if "trkRecoilStrength" in parsed_config:
            var_trkRecoilStrength.set(parsed_config["trkRecoilStrength"])
        if "radTriggerRecoil" in parsed_config:
            var_radTriggerRecoil.set(parsed_config["radTriggerRecoil"])
        if "trkRecoilSlider" in parsed_config:
            var_trkRecoilSlider.set(parsed_config["trkRecoilSlider"])
        if "trkStartDelay" in parsed_config:
            var_trkStartDelay.set(parsed_config["trkStartDelay"])
        if "trkDelayBetweenPulses" in parsed_config:
            var_trkDelayBetweenPulses.set(parsed_config["trkDelayBetweenPulses"])

        messagebox.showinfo("Import", "Recoil configuration values imported!")
    except Exception as e:
        messagebox.showerror("Import Error", f"An error occurred during import:\n{e}")



def recoilexportToSinden():
    """
    Gather recoil settings from various controls, update the Lightgun.exe.config file
    by replacing settings in the file (which is treated as a plain text file), and
    display a message confirming the export.
    """
    # Gather settings from the controls.
    settings = {
        "chkRecoilTerms": var_chkRecoilTerms.get(),
        "chkEnableRecoil": var_chkEnableRecoil.get(),
        "chkRecoilTrigger": var_chkRecoilTrigger.get(),
        "chkRecoilTriggerOffscreen": var_chkRecoilTriggerOffscreen.get(),
        "chkRecoilPumpActionOnEvent": var_chkRecoilPumpActionOnEvent.get(),
        "chkRecoilPumpActionOffEvent": var_chkRecoilPumpActionOffEvent.get(),
        "chkRecoilFrontLeft": var_chkRecoilFrontLeft.get(),
        "chkRecoilFrontRight": var_chkRecoilFrontRight.get(),
        "chkRecoilBackLeft": var_chkRecoilBackLeft.get(),
        "chkRecoilBackRight": var_chkRecoilBackRight.get(),
        "chkRecoilAlternative": var_chkRecoilAlternative.get(),
        "trkRecoilStrength": var_trkRecoilStrength.get(),
        "radTriggerRecoil": var_radTriggerRecoil.get(),  # 1 for Normal; 0 for Repeat
        "trkRecoilSlider": var_trkRecoilSlider.get(),
        "trkStartDelay": var_trkStartDelay.get(),
        "trkDelayBetweenPulses": var_trkDelayBetweenPulses.get(),
    }
    
    config_file = "Lightgun.exe.config"
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load config file: {e}")
        return

    # For each key-value pair, perform a regex substitution.
    # This pattern matches lines like:
    #     <add key="chkRecoilTerms" value="1" />
    # and replaces the value part.
    for key, value in settings.items():
        pattern = fr'(<add\s+key="{re.escape(key)}"\s+value=")(.*?)(".*?>)'
        # Replace group 2 (the old value) with the new value (converted to string).
        content, subs = re.subn(pattern, r'\1' + str(value) + r'\3', content)
        # Optionally, you can check if subs == 0 to warn that the key was not found.
    
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Export", "Recoil configuration values exported and config file updated!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write config file: {e}")


# ---------------------------
# TKINTER VARIABLES
# ---------------------------

# Checkbox variables
var_chkRecoilTerms = tk.IntVar(value=10)
var_chkEnableRecoil = tk.IntVar(value=0)
var_chkRecoilTrigger = tk.IntVar(value=1)
var_chkRecoilTriggerOffscreen = tk.IntVar(value=1)
var_chkRecoilPumpActionOnEvent = tk.IntVar(value=0)
var_chkRecoilPumpActionOffEvent = tk.IntVar(value=0)
var_chkRecoilFrontLeft = tk.IntVar(value=1)
var_chkRecoilFrontRight = tk.IntVar(value=0)
var_chkRecoilBackLeft = tk.IntVar(value=0)
var_chkRecoilBackRight = tk.IntVar(value=0)
var_chkRecoilAlternative = tk.IntVar(value=0)

# Slider (trackbar) variables
var_trkRecoilStrength = tk.IntVar(value=10)
var_trkRecoilSlider = tk.IntVar(value=75)
var_trkStartDelay = tk.IntVar(value=0)
var_trkDelayBetweenPulses = tk.IntVar(value=13)






# Radiobutton variable (1 for Normal; 0 for Repeat)
var_radTriggerRecoil = tk.IntVar(value=1)


# Create a Notebook tab named "Recoil"
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Recoil")

# Configure grid for tab2 for a consistent layout.
tab2.columnconfigure(0, weight=1)

# ---------------------------
# LAYOUT ON tab2
# ---------------------------
folder_path = "./SRS Configs/Recoil"  # dummy/fallback; list_files uses a hard-coded folder.
# 2. Place the Text widget immediately after the button.
text = tk.Text(tab2, wrap="none", height=7, width=45)
text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
text.bind("<Button-1>", on_click)
list_files(folder_path)  # Populate the Text widget with files.

# 3. Create a frame for the recoil controls that appears below the Text widget.
config_frameR = ttk.Frame(tab2)
config_frameR.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
config_frameR.columnconfigure(0, weight=1)

# 1. Export to Sinden button at the top.
# (The folder_path argument is not used inside list_files in this example.)

export_button = ttk.Button(config_frameR, text="Push Recoil Config to Sinden", command=recoilexportToSinden)
export_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Add an export button for recoil settings in config_frameR.
btn_export = ttk.Button(config_frameR, text="Export Recoil Config", command=recoilexport_values)
btn_export.grid(row=0, column=0, padx=10, pady=10, sticky="w", columnspan=3)

# Create separate labeled frames within config_frameR to group controls.
chk_frame = ttk.LabelFrame(config_frameR, text="Checkbox Options", padding=10)
chk_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

scale_frame = ttk.LabelFrame(config_frameR, text="Slider Options", padding=10)
scale_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ne")

radio_frame = ttk.LabelFrame(config_frameR, text="Trigger Recoil Mode", padding=10)
radio_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w", columnspan=2)

# ---------------------------
# RECOIL CONTROLS
# ---------------------------
# Checkbox Controls
tk.Checkbutton(chk_frame, text="Recoil Terms", variable=var_chkRecoilTerms).grid(row=0, column=0, sticky="w")
tk.Checkbutton(chk_frame, text="Enable Recoil", variable=var_chkEnableRecoil).grid(row=1, column=0, sticky="w")
tk.Checkbutton(chk_frame, text="Recoil Trigger", variable=var_chkRecoilTrigger).grid(row=2, column=0, sticky="w")
tk.Checkbutton(chk_frame, text="Recoil Trigger Offscreen", variable=var_chkRecoilTriggerOffscreen).grid(row=3, column=0, sticky="w")
tk.Checkbutton(chk_frame, text="Pump Action On Event", variable=var_chkRecoilPumpActionOnEvent).grid(row=4, column=0, sticky="w")
tk.Checkbutton(chk_frame, text="Pump Action Off Event", variable=var_chkRecoilPumpActionOffEvent).grid(row=5, column=0, sticky="w")
tk.Checkbutton(chk_frame, text="Recoil Front Left", variable=var_chkRecoilFrontLeft).grid(row=6, column=0, sticky="w")
tk.Checkbutton(chk_frame, text="Recoil Front Right", variable=var_chkRecoilFrontRight).grid(row=7, column=0, sticky="w")
tk.Checkbutton(chk_frame, text="Recoil Back Left", variable=var_chkRecoilBackLeft).grid(row=8, column=0, sticky="w")
tk.Checkbutton(chk_frame, text="Recoil Back Right", variable=var_chkRecoilBackRight).grid(row=9, column=0, sticky="w")
tk.Checkbutton(chk_frame, text="Recoil Alternative", variable=var_chkRecoilAlternative).grid(row=10, column=0, sticky="w")

# Slider Controls
tk.Scale(scale_frame, label="Recoil Strength", from_=0, to=100, orient="horizontal",
         variable=var_trkRecoilStrength).grid(row=0, column=0, sticky="ew", padx=5, pady=5)
tk.Scale(scale_frame, label="Recoil Slider", from_=0, to=100, orient="horizontal",
         variable=var_trkRecoilSlider).grid(row=1, column=0, sticky="ew", padx=5, pady=5)
tk.Scale(scale_frame, label="Start Delay", from_=0, to=100, orient="horizontal",
         variable=var_trkStartDelay).grid(row=2, column=0, sticky="ew", padx=5, pady=5)
tk.Scale(scale_frame, label="Delay Between Pulses", from_=0, to=100, orient="horizontal",
         variable=var_trkDelayBetweenPulses).grid(row=3, column=0, sticky="ew", padx=5, pady=5)

# Radiobutton Controls
tk.Radiobutton(radio_frame, text="Trigger Recoil Normal", variable=var_radTriggerRecoil, value=1)\
    .grid(row=0, column=0, padx=5, pady=5, sticky="w")
tk.Radiobutton(radio_frame, text="Trigger Recoil Repeat", variable=var_radTriggerRecoil, value=0)\
    .grid(row=0, column=1, padx=5, pady=5, sticky="w")


### TAB 3

global games
global gamecodes
global gameselection

games = ["RESIDENT EVIL THE DARKSIDE CHRONICLES", "RESIDENT EVIL THE DARKSIDE CHRONICLES","RESIDENT EVIL THE DARKSIDE CHRONICLES","RESIDENT EVIL THE DARKSIDE CHRONICLES",
         "RESIDENT EVIL THE UMBRELLA CHRONICLES",
         "TRAUMA CENTER NEW BLOOD","TRAUMA CENTER NEW BLOOD","TRAUMA CENTER NEW BLOOD"]



gamecodes = ["SBDE08", "SBDJ08", "SBDK08", "SBDP08",
             "RBUE08",
             "RK2EEB", "RK2JEB", "RK2P01"]

# Tab 3 Dolphin functions
def dolphingame_click(event):
    """
    Get the selected item from the Listbox and print it.
    """
    global gameselection
    # Get the current selection via curselection(), which returns a tuple of indices.
    selection = listbox2.curselection()
    if selection:
        index = selection[0]  # Get the first selected index.
        gameselection = listbox2.get(index).strip()  # Retrieve the item text.
        print("Clicked on: " + gameselection)



tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Dolphin Export Mappings")
 # Create a horizontal frame to hold the file path controls in Tab 3

####
####### DOLPHIN MAPPING
####Add a label and multiline listbox with options A, B, and C
label = tk.Label(tab3, text="Dolphin Games: Select a Wii Game:")
label.pack(pady=5)

# Here, we use a Listbox widget which provides multiple lines of data
listbox2 = tk.Listbox(tab3, height=3, width = 40)


for option in games:
    current_items = listbox2.get(0, tk.END)
    if option not in current_items:
        listbox2.insert(tk.END, option)
        
listbox2.pack(pady=5)

# Bind the selection event to the on_select handler
listbox2.bind("<<ListboxSelect>>", dolphingame_click)

 

### DOLPHIN FILE PATHS
redswitch = "N"
style = ttk.Style()
style.configure("Red.TLabel", foreground="red")



global dolphin_path
def find_prog(prog):
    return shutil.which(prog)

# Example usage:
path = find_prog("dolphin.exe")
if path:
    print(f"Found at: {path}")
else:
    print("Program not found.")




dolphin_path = shutil.which("dolphin.exe")
if dolphin_path:
    print("Found dolphin.exe at:", dolphin_path)
else:
    
    print("dolphin.exe was not found in your system PATH.")
    dolphin_path = os.getcwd()
    redswitch = "Y"

dolphinGameSettingExportPath = "Game Settings Path To Be Updated"
if redswitch != "Y":
    dolphinGameSettingExportPath = os.path.join(dolphin_path, r"\User\GameSettings\ ")


dolphinControllerExportPath ="Controller Settings Path To Be Updated"
if redswitch != "Y":
    dolphinControllerExportPath = os.path.join(dolphin_path, fr"\User\Config\Profiles\WiiMote\ ")

#####Mapping functions

def export_game_mapping():
		  
    for game, gamecode in zip(games, gamecodes):
        if gameselection == game:


        # Define the content to write to the file
            content = '[Controls]\n'+'#'+game+"-"+gamecode+'\n'
            content += "WiimoteProfile1 = SRS " + game +'\n'

        # Write the content to the file (overwriting the existing content)
            try:
                if not os.path.exists(os.path.abspath(dolphinGameSettingExportPath+gamecode+'.ini')):
                    with open(os.path.abspath(dolphinGameSettingExportPath+gamecode+'.ini'), 'w') as file:
                        file.write(content)
                        print(f"File has been overwritten successfully.")
            except FileNotFoundError:
                print(f"File not found.")
            except Exception as e:
                print(f"An error occurred: {e}")


def export_dolphin_mapping():
		
    for game, gamecode in zip(games, gamecodes):
        content = ""
        # Define the content to write to the file
        if game == "":
            #Mario Kart Double Dash
           content = ("""
[Profile]
Device = DInput/0/Keyboard Mouse
Buttons/A = `Click 2`
Buttons/1 = `1`
Buttons/2 = `2`
Buttons/- = Q
Buttons/+ = E
Buttons/Home = RETURN
D-Pad/Up = UP
D-Pad/Down = DOWN
D-Pad/Left = LEFT
D-Pad/Right = RIGHT
IR/Up = `Cursor Y-`
IR/Down = `Cursor Y+`
IR/Left = `Cursor X-`
IR/Right = `Cursor X+`
Shake/X = `Click 2`
Shake/Y = `Click 2`
Shake/Z = `Click 2`
IRPassthrough/Object 1 X = `IR Object 1 X`
IRPassthrough/Object 1 Y = `IR Object 1 Y`
IRPassthrough/Object 1 Size = `IR Object 1 Size`
IRPassthrough/Object 2 X = `IR Object 2 X`
IRPassthrough/Object 2 Y = `IR Object 2 Y`
IRPassthrough/Object 2 Size = `IR Object 2 Size`
IRPassthrough/Object 3 X = `IR Object 3 X`
IRPassthrough/Object 3 Y = `IR Object 3 Y`
IRPassthrough/Object 3 Size = `IR Object 3 Size`
IRPassthrough/Object 4 X = `IR Object 4 X`
IRPassthrough/Object 4 Y = `IR Object 4 Y`
IRPassthrough/Object 4 Size = `IR Object 4 Size`
IMUAccelerometer/Up = `Accel Up`
IMUAccelerometer/Down = `Accel Down`
IMUAccelerometer/Left = `Accel Left`
IMUAccelerometer/Right = `Accel Right`
IMUAccelerometer/Forward = `Accel Forward`
IMUAccelerometer/Backward = `Accel Backward`
IMUGyroscope/Pitch Up = `Gyro Pitch Up`
IMUGyroscope/Pitch Down = `Gyro Pitch Down`
IMUGyroscope/Roll Left = `Gyro Roll Left`
IMUGyroscope/Roll Right = `Gyro Roll Right`
IMUGyroscope/Yaw Left = `Gyro Yaw Left`
IMUGyroscope/Yaw Right = `Gyro Yaw Right`
Extension = Nunchuk
Nunchuk/Buttons/C = LCONTROL
Nunchuk/Buttons/Z = LSHIFT
Nunchuk/Stick/Up = W
Nunchuk/Stick/Down = S
Nunchuk/Stick/Left = A
Nunchuk/Stick/Right = D
Nunchuk/Stick/Calibration = 100.00 141.42 100.00 141.42 100.00 141.42 100.00 141.42
Nunchuk/Shake/X = `Click 2`
Nunchuk/Shake/Y = `Click 2`
Nunchuk/Shake/Z = `Click 2`

""")
        elif game == "TRAUMA CENTER NEW BLOOD":
           content = ("""
[Profile]
Device = DInput/0/Keyboard Mouse
Buttons/A = A
Buttons/B = B
Buttons/1 = `1`
Buttons/2 = `2`
Buttons/- = MINUS
Buttons/+ = @(Shift+EQUALS)
Buttons/Home = RETURN
D-Pad/Up = UP
D-Pad/Down = DOWN
D-Pad/Left = LEFT
D-Pad/Right = RIGHT
IR/Up = `Cursor Y-`
IR/Down = `Cursor Y+`
IR/Left = `Cursor X-`
IR/Right = `Cursor X+`
Shake/X = `Click 2`
Shake/Y = `Click 2`
Shake/Z = `Click 2`
IRPassthrough/Object 1 X = `IR Object 1 X`
IRPassthrough/Object 1 Y = `IR Object 1 Y`
IRPassthrough/Object 1 Size = `IR Object 1 Size`
IRPassthrough/Object 2 X = `IR Object 2 X`
IRPassthrough/Object 2 Y = `IR Object 2 Y`
IRPassthrough/Object 2 Size = `IR Object 2 Size`
IRPassthrough/Object 3 X = `IR Object 3 X`
IRPassthrough/Object 3 Y = `IR Object 3 Y`
IRPassthrough/Object 3 Size = `IR Object 3 Size`
IRPassthrough/Object 4 X = `IR Object 4 X`
IRPassthrough/Object 4 Y = `IR Object 4 Y`
IRPassthrough/Object 4 Size = `IR Object 4 Size`
IMUAccelerometer/Up = `Accel Up`
IMUAccelerometer/Down = `Accel Down`
IMUAccelerometer/Left = `Accel Left`
IMUAccelerometer/Right = `Accel Right`
IMUAccelerometer/Forward = `Accel Forward`
IMUAccelerometer/Backward = `Accel Backward`
IMUGyroscope/Pitch Up = `Gyro Pitch Up`
IMUGyroscope/Pitch Down = `Gyro Pitch Down`
IMUGyroscope/Roll Left = `Gyro Roll Left`
IMUGyroscope/Roll Right = `Gyro Roll Right`
IMUGyroscope/Yaw Left = `Gyro Yaw Left`
IMUGyroscope/Yaw Right = `Gyro Yaw Right`
Extension = Nunchuk
Nunchuk/Buttons/C = C
Nunchuk/Buttons/Z = Z
Nunchuk/Stick/Up = W
Nunchuk/Stick/Down = S
Nunchuk/Stick/Left = Z
Nunchuk/Stick/Right = D
Nunchuk/Stick/Calibration = 100.00 141.42 100.00 141.42 100.00 141.42 100.00 141.42
Nunchuk/Shake/X = `Click 2`
Nunchuk/Shake/Y = `Click 2`
Nunchuk/Shake/Z = `Click 2`
""")


    if content != "":
        # Write the content to the file (overwriting the existing content)
        try:
            if not os.path.exists(os.path.abspath(dolphinControllerExportPath+gamecode+'.ini')):
                with open(os.path.abspath(dolphinControllerExportPath+gamecode + '.ini'), 'w') as file:
                    file.write(content)
                    print(f"File has been overwritten successfully.")
        except FileNotFoundError:
            print(f"File not found.")
        except Exception as e:
            print(f"An error occurred: {e}")   

### Dolphin location
 # Create a horizontal frame to hold the file path controls in Tab 3

 
hframedolphin = ttk.Frame(tab3)
hframedolphin.pack(pady=5)
    
# Create a label in the horizontal frame
dolphinloclabel = ttk.Label(hframedolphin, text="Dolphin File Path Location:")
dolphinloclabel.pack(side="left", padx=5)
       
# Create an Entry widget to display the file path (initially set as read-only)
dolphinpath_entry = ttk.Entry(hframedolphin, width=80)
if redswitch == "Y":  # Assuming redswitch is defined elsewhere as "Y"
    dolphinpath_entry.config(style="Red.TLabel")
dolphinpath_entry.pack(side="left", padx=5)
dolphinpath_entry.insert(0, dolphin_path)
dolphinpath_entry.config(state="readonly")

def change_dpath():
    global dolphin_path  # Ensure we update the global variable
    # Open a dialog to let the user select a new directory
    new_path = filedialog.askdirectory(title="Select a New Directory")
    print("Old path:", dolphin_path)
    print("New path:", new_path)
    if new_path:  # if a new directory is selected (new_path is not empty)
        dolphin_path = new_path  # update global variable
        # Enable editing, update the path, then set back to read-only
        dolphinpath_entry.config(state='normal')
        dolphinpath_entry.delete(0, tk.END)
        dolphinpath_entry.insert(0, new_path)
        dolphinpath_entry.update_idletasks()  # Force an immediate refresh
        dolphinpath_entry.config(state='readonly')
        
        path_entry.config(state='normal')
        dolphinGameSettingExportPath = os.path.join(dolphin_path, "User", "GameSettings")
        path_entry.config(state='normal')
        path_entry.delete(0, tk.END)
        path_entry.insert(0, dolphinGameSettingExportPath)
        path_entry.config(state='readonly')
        
        controllerpath_entry.config(state='normal')
        dolphinControllerExportPath = os.path.join(dolphin_path, "User", "Config", "Profiles", "WiiMote")
        controllerpath_entry.delete(0, tk.END)
        controllerpath_entry.insert(0, dolphinControllerExportPath)
        controllerpath_entry.config(state='readonly')

        print("Game Settings Path:", dolphinGameSettingExportPath)
        print("Controller Export Path:", dolphinControllerExportPath)

# Create a button that lets the user change the path
dolphinchange_button = ttk.Button(hframedolphin, text="Change Path", command=change_dpath)
dolphinchange_button.pack(side="left", padx=5)



###### Game Mapping Path

hframe = ttk.Frame(tab3)
hframe.pack(pady=20)
    
# Create a label in the horizontal frame
dolphinlabel = ttk.Label(hframe, text="Game File Path:")
dolphinlabel.pack(side="left", padx=5)
    
    # Create an Entry widget to display the file path (initially set as read-only)
path_entry = ttk.Entry(hframe, width=80)
path_entry.pack(side="left", padx=5)
path_entry.insert(0, dolphinGameSettingExportPath)
path_entry.config(state="readonly")

def change_gspath():
    # Open a dialog to let the user select a new directory
    dolphinGameSettingExportPath = filedialog.askdirectory(title="Select a New Directory")
    if dolphinGameSettingExportPath:
        # Enable editing, update the path, then set back to read-only
        path_entry.config(state='normal')
        path_entry.delete(0, tk.END)
        path_entry.insert(0, dolphinGameSettingExportPath)
        path_entry.config(state='readonly')


    # Create a button that lets the user change the path
change_button = ttk.Button(hframe, text="Change Path", command=change_gspath)
change_button.pack(side="left", padx=5)

btn_game = ttk.Button(hframe, text="Export Game Mapping", command=export_game_mapping)
btn_game.pack(pady=5)



###### Controller Mapping Path
hframefirst = ttk.Frame(tab3)
hframefirst.pack(pady=5)

# Create a label in the horizontal frame
controllerLabelPath = ttk.Label(hframefirst, text="Controller Mapping Path:")
controllerLabelPath.pack(side="left", padx=5)

    # Create an Entry widget to display the file path (initially set as read-only)
controllerpath_entry = ttk.Entry(hframefirst, width=80)
controllerpath_entry.pack(side="left", padx=5)
controllerpath_entry.insert(0, dolphinControllerExportPath)
controllerpath_entry.config(state="readonly")

def change_controllerpath():
    # Open a dialog to let the user select a new directory
    dolphinGameSettingExportPath = filedialog.askdirectory(title="Select a New Directory")
    if dolphinControllerExportPath:
        # Enable editing, update the path, then set back to read-only
        controllerpath_entry.config(state='normal')
        controllerpath_entry.delete(0, tk.END)
        controllerpath_entry.insert(0, dolphinControllerExportPath)
        controllerpath_entry.config(state='readonly')
    print("Game Settings Path:", dolphinGameSettingExportPath)

# Add buttons to the third tab
    # Create a button that lets the user change the path
controllerchange_button = ttk.Button(hframefirst, text="Change Path", command=change_controllerpath)
controllerchange_button.pack(side="left", padx=5)



btn_dolphin = ttk.Button(hframefirst, text="Export Dolphin Controller Mapping", command=export_dolphin_mapping)
btn_dolphin.pack(pady=10)

hframelast = ttk.Frame(tab3)
hframelast.pack(pady=25)

def start_dolphin():
    # Specify the full path if dolphin.exe is not in your system's PATH,
    # for example: r"C:\Program Files\Dolphin\Dolphin.exe".
    print(dolphin_path)
    dolphinpathstart = os.path.join(dolphin_path, "dolphin.exe")
    print(dolphinpathstart)
    try:
        # Using subprocess.Popen so that your application remains responsive.
        subprocess.Popen([dolphinpathstart])
    except Exception as e:
        print(f"Error starting {dolphinpathstart}: {e}")


btn_startdolphin = ttk.Button(hframelast, text="Start Dolphin", command=start_dolphin)
btn_startdolphin.pack(pady=25)
    

# ---------------------------
# START THE APPLICATION
# ---------------------------

root.mainloop()
