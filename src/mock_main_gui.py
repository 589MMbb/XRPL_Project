import tkinter as tk
from tkinter import messagebox

def mock_building_data():
    messagebox.showinfo("Building Data", "This would launch the Building Data module.")

def mock_air_rights_calculation():
    messagebox.showinfo("Air Rights Calculation", "This would launch the Air Rights Calculation module.")

def mock_nft_minting():
    messagebox.showinfo("NFT Minting", "This would launch the NFT Minting module.")


root = tk.Tk()
root.title("Building Data and NFT Minting Prototype")


btn_building_data = tk.Button(root, text="Enter Building Data", command=mock_building_data)
btn_building_data.pack(pady=10)


btn_air_rights = tk.Button(root, text="Calculate Air Rights", command=mock_air_rights_calculation)
btn_air_rights.pack(pady=10)


btn_nft_minting = tk.Button(root, text="Mint NFT", command=mock_nft_minting)
btn_nft_minting.pack(pady=10)

root.mainloop()
