import tkinter as tk
from tkinter import messagebox
import json
import building_data 
import air_rights_gui  
import nft_minting  

def launch_building_data():
    
    building_data.main()

def launch_air_rights_calculation():

    air_rights_gui.main()

def launch_nft_minting():

    nft_minting.main()

root = tk.Tk()
root.title("Building Data and NFT Minting Interface")


building_data_btn = tk.Button(root, text="Enter Building Data", command=launch_building_data)
building_data_btn.pack(pady=10)


air_rights_btn = tk.Button(root, text="Calculate Air Rights", command=launch_air_rights_calculation)
air_rights_btn.pack(pady=10)


nft_minting_btn = tk.Button(root, text="Mint NFT", command=launch_nft_minting)
nft_minting_btn.pack(pady=10)

root.mainloop()
