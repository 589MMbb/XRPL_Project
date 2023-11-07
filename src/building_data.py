import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

JSON_PATH = "building_data.json"

def save_building_data():
    building_name = name_entry.get()
    if not building_name:
        messagebox.showerror("Error", "Please provide a building name or address.")
        return

    new_data = {
        building_name: {
            "zoning": zoning_entry.get(),
            "landArea": land_area_entry.get(),
            "otherDetails": other_details_entry.get()
        }
    }

    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    data.update(new_data)

    with open(JSON_PATH, 'w') as file:
        json.dump(data, file, indent=4)

    messagebox.showinfo("Success", "Building data saved successfully!")
    refresh_display()


def refresh_display():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    building_address_combobox["values"] = list(data.keys())
    display_text.delete(1.0, tk.END)
    for building, details in data.items():
        display_text.insert(tk.END, f"Building Name: {building}\n")
        for key, value in details.items():
            display_text.insert(tk.END, f"{key}: {value}\n")
        display_text.insert(tk.END, "-"*40 + "\n")

def on_address_select(event):
    building = building_address_combobox.get()
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r') as file:
            data = json.load(file)
            details = data.get(building, {})
            name_entry.delete(0, tk.END)
            name_entry.insert(0, building)
            zoning_entry.delete(0, tk.END)
            zoning_entry.insert(0, details.get("zoning", ""))
            land_area_entry.delete(0, tk.END)
            land_area_entry.insert(0, details.get("landArea", ""))
            other_details_entry.delete(0, tk.END)
            other_details_entry.insert(0, details.get("otherDetails", ""))

window = tk.Tk()
window.title("Building Data Manager")


building_address_combobox = ttk.Combobox(window, postcommand=refresh_display)
building_address_combobox.pack(pady=10)
building_address_combobox.bind("<<ComboboxSelected>>", on_address_select)


label_name = tk.Label(window, text="Building Name:")
label_name.pack(pady=10)
name_entry = tk.Entry(window)
name_entry.pack(pady=10)


label_zoning = tk.Label(window, text="Zoning:")
label_zoning.pack(pady=10)
zoning_entry = tk.Entry(window)
zoning_entry.pack(pady=10)


label_land_area = tk.Label(window, text="Land Area:")
label_land_area.pack(pady=10)
land_area_entry = tk.Entry(window)
land_area_entry.pack(pady=10)


label_other_details = tk.Label(window, text="Other Details:")
label_other_details.pack(pady=10)
other_details_entry = tk.Entry(window)
other_details_entry.pack(pady=10)


save_button = tk.Button(window, text="Save Building Data", command=save_building_data)
save_button.pack(pady=20)


display_text = tk.Text(window, width=60, height=20)
display_text.pack(pady=20)

refresh_display() 

window.mainloop()
