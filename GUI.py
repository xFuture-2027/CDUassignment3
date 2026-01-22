import tkinter as tk
from tkinter import ttk

class GUI:
    """class for setting up all GUI components, we separate the GUI design 
    from application logic for clean code"""
    @staticmethod
    def setup_menu(root,callbacks):
        """ create the menu bar with FIle and Edit menus"""
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar,tearoff=0)
        
        menubar.add_cascade(label="File",menu=file_menu)
        menubar.add_command(
            label="open",
            command=callback['open_image'],
            accelerator = "Ctrl+O"
            )
            