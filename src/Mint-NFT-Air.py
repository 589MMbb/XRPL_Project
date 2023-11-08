import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Constants for file paths
BUILDING_DATA_JSON_PATH = "building_data.json"
AIR_RIGHTS_OUTPUT_JSON_PATH = "air_rights_output.json"
COMBINED_NFT_METADATA_JSON_PATH = "CombinedNFTMetadata.json"

# Mock function to get XRP price
def get_xrp_price():
    return 0.5  # Example static price

# Function to load building data
def load_building_data():
    if os.path.exists(BUILDING_DATA_JSON_PATH):
        with open(BUILDING_DATA_JSON_PATH, 'r') as file:
            return json.load(file)
    return {}

# Function to save building data
def save_building_data():
    building_name = building_name_entry.get()
    zoning = zoning_entry.get()
    land_area = land_area_entry.get()
    other_details = other_details_entry.get()

    new_data = {
        building_name: {
            "zoning": zoning,
            "landArea": land_area,
            "otherDetails": other_details
        }
    }
    data = load_building_data()
    data.update(new_data)
    with open(BUILDING_DATA_JSON_PATH, 'w') as file:
        json.dump(data, file, indent=4)
    messagebox.showinfo("Success", "Building data saved successfully!")
    refresh_building_list()

# Function to refresh the building list in the GUI
def refresh_building_list():
    building_list = list(load_building_data().keys())
    building_combobox['values'] = building_list
    if building_list:
        building_combobox.set(building_list[0])

# Function to calculate and display air rights with more details
def calculate_and_display_air_rights():
    try:
        existing_sqft = float(existing_sqft_entry.get())
        max_buildable_sqft = float(max_buildable_sqft_entry.get())
        if max_buildable_sqft <= existing_sqft:
            raise ValueError("Max buildable square footage must be greater than existing square footage.")
        
        # Placeholder calculation for air rights
        air_rights = max_buildable_sqft - existing_sqft
        xrp_price = get_xrp_price()
        air_rights_value_usd = air_rights * 100  # Example calculation
        air_rights_value_xrp = air_rights_value_usd / xrp_price

        # Display the calculated air rights in the status text area
        status_text.insert(tk.END, f"Air rights (USD): ${air_rights_value_usd:,.2f}\n")
        status_text.insert(tk.END, f"Air rights (XRP): {air_rights_value_xrp:,.2f} XRP\n")

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Function to generate NFT metadata with more details in the text area
def generate_metadata():
    status_text.insert(tk.END, "Generating NFT metadata...\n")
    # Placeholder logic to generate metadata
    # Here you would generate and save the NFT metadata, then update the status
    status_text.insert(tk.END, "NFT metadata generated successfully.\n")

# Function to mint the NFT with more details in the text area
def mint_the_nft():
    status_text.insert(tk.END, "Minting NFT on the XRPL Testnet...\n")
    # Placeholder logic to mint NFT
    # Here you would mint the NFT using the XRPL library functions, then update the status
    status_text.insert(tk.END, "NFT minted successfully with TX ID: 1234567890\n")

# GUI setup
root = tk.Tk()
root.title("Complete NFT Workflow")

# Building data entry fields
tk.Label(root, text="Building Name:").pack()
building_name_entry = tk.Entry(root)
building_name_entry.pack()

tk.Label(root, text="Zoning:").pack()
zoning_entry = tk.Entry(root)
zoning_entry.pack()

tk.Label(root, text="Land Area:").pack()
land_area_entry = tk.Entry(root)
land_area_entry.pack()

tk.Label(root, text="Other Details:").pack()
other_details_entry = tk.Entry(root)
other_details_entry.pack()

# Button to save building data
button_save = tk.Button(root, text="Save Building Data", command=save_building_data)
button_save.pack()

# Combobox to select building for air rights calculation
tk.Label(root, text="Select Building:").pack()
building_combobox = ttk.Combobox(root, postcommand=refresh_building_list)
building_combobox.pack()

# Entry fields for existing and maximum buildable square footage
tk.Label(root, text="Existing Sq Ft:").pack()
existing_sqft_entry = tk.Entry(root)
existing_sqft_entry.pack()

tk.Label(root, text="Max Buildable Sq Ft:").pack()
max_buildable_sqft_entry = tk.Entry(root)
max_buildable_sqft_entry.pack()

# Button to calculate and display air rights
button_calculate = tk.Button(root, text="Calculate Air Rights", command=calculate_and_display_air_rights)
button_calculate.pack()

# Button to generate NFT metadata
button_generate_metadata = tk.Button(root, text="Generate NFT Metadata", command=generate_metadata)
button_generate_metadata.pack()

# Button to mint NFT
button_mint_nft = tk.Button(root, text="Mint NFT", command=mint_the_nft)
button_mint_nft.pack()

# Status display
status_text = tk.Text(root, height=10, width=50)
status_text.pack()

# Initialize the building list
refresh_building_list()

root.mainloop()
