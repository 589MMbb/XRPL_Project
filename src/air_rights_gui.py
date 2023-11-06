import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

from xrp_price import get_xrp_price

JSON_PATH = "building_data.json"
OUTPUT_PATH = "air_rights_output.json"

def load_building_data():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r') as file:
            return json.load(file)
    return {}

def create_scale(frame, row, text, from_=0, to_=100):
    label = ttk.Label(frame, text=text)
    label.grid(row=row, column=0, sticky='w')
    
    scale = ttk.Scale(frame, from_=from_, to=to_, orient="horizontal")
    scale.grid(row=row, column=1)
    
    value_label = ttk.Label(frame, text="%.2f" % scale.get())
    value_label.grid(row=row, column=2)
    
    def update_label(event):
        value_label.config(text="%.2f" % scale.get())
    
    scale.bind('<Motion>', update_label)
    
    return scale, value_label


def update_label(scale_value, label):
    label.config(text=f"{float(scale_value):.2f}")

def on_building_select(event):
    building = building_combobox.get()
    building_data = load_building_data()
    details = building_data.get(building, {})
    max_buildable_sqft_entry.delete(0, tk.END)
    max_buildable_sqft_entry.insert(0, details.get("landArea", ""))

def calculate_air_rights_value(baseline, factors, max_buildable_sqft, existing_sqft, xrp_price):
    air_rights = max_buildable_sqft - existing_sqft
    if air_rights <= 0:
        raise ValueError("The existing building square footage exceeds or equals the max buildable square footage.")
    air_rights_value = baseline * air_rights
    for factor in factors:
        air_rights_value *= factor
    return {
        "air_rights_usd": air_rights_value,
        "air_rights_xrp": air_rights_value / xrp_price
    }

def get_values_and_calculate():
    try:
        # Fetch the current XRP price using your custom function
        xrp_current_price = get_xrp_price()

        # Get the values from the GUI inputs
        baseline = float(baseline_entry.get())
        factor1_value = factor1_scale.get()
        factor2_value = factor2_scale.get()
        factor3_value = factor3_scale.get()
        factors = [factor1_value, factor2_value, factor3_value]
        max_buildable_sqft = float(max_buildable_sqft_entry.get())
        existing_sqft = float(existing_sqft_entry.get())

        # Calculate the air rights value using the provided factors
        air_rights_value = calculate_air_rights_value(baseline, factors, max_buildable_sqft, existing_sqft, xrp_current_price)

        # Format the results to display in the GUI
        formatted_air_rights_value = "{:,.2f}".format(air_rights_value['air_rights_usd'])
        formatted_xrp_value = "{:,.2f}".format(air_rights_value['air_rights_xrp'])

        # Update the result label with the formatted values
        result_label.config(text=f"Air Rights Value: ${formatted_air_rights_value} or {formatted_xrp_value} XRP")
    except Exception as e:
        # If an error occurs, show it in a messagebox and update the result label
        messagebox.showerror("Error", str(e))
        result_label.config(text=f"Error: {str(e)}")

def export_to_json(data):
    with open(OUTPUT_PATH, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    messagebox.showinfo("Export Successful", f"Data has been exported to {OUTPUT_PATH}")

def get_values_and_export():
    get_values_and_calculate() 
    try:
        building = building_combobox.get()
        air_rights_data = {
            "building": building,
            "air_rights_value": calculate_air_rights_value(
                float(baseline_entry.get()),
                [factor1_scale.get(), factor2_scale.get(), factor3_scale.get()],
                float(max_buildable_sqft_entry.get()),
                float(existing_sqft_entry.get()),
                get_xrp_price()
            )
        }
        export_to_json(air_rights_data)
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Air Rights Calculator")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

building_label = ttk.Label(frame, text="Select Building:")
building_label.grid(row=0, column=0, sticky=tk.W, pady=5)
building_combobox = ttk.Combobox(frame, values=list(load_building_data().keys()))
building_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
building_combobox.bind('<<ComboboxSelected>>', on_building_select)

baseline_label = ttk.Label(frame, text="Baseline Value:")
baseline_label.grid(row=1, column=0, sticky=tk.W, pady=5)
baseline_entry = ttk.Entry(frame)
baseline_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

factor1_scale, factor1_value_label = create_scale(frame, 2, "Accessibility Factor:", 0.5, 1.5)
factor2_scale, factor2_value_label = create_scale(frame, 3, "Neighborhood Factor:", 0.5, 1.5)
factor3_scale, factor3_value_label = create_scale(frame, 4, "Market Factor:", 0.5, 1.5)

max_buildable_sqft_label = ttk.Label(frame, text="Max Buildable SqFt:")
max_buildable_sqft_label.grid(row=5, column=0, sticky=tk.W, pady=5)
max_buildable_sqft_entry = ttk.Entry(frame)
max_buildable_sqft_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)

existing_sqft_label = ttk.Label(frame, text="Existing Building SqFt:")
existing_sqft_label.grid(row=6, column=0, sticky=tk.W, pady=5)
existing_sqft_entry = ttk.Entry(frame)
existing_sqft_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5)

calculate_button = ttk.Button(frame, text="Calculate", command=get_values_and_calculate)
calculate_button.grid(row=7, column=1, pady=15)

export_button = ttk.Button(frame, text="Export to JSON", command=get_values_and_export)
export_button.grid(row=8, column=1, pady=15)

result_label = ttk.Label(frame, text="Air Rights Value:")
result_label.grid(row=9, column=0, columnspan=3)

root.mainloop()
