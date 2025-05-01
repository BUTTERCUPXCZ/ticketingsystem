import tkinter as tk
from tkinter import ttk

class EmptyState(tk.Frame):
    def __init__(self, parent, icon="📭", title="No items found", 
                 subtitle="There are no items to display"):
        super().__init__(parent, bg=parent["bg"])
        
        # Icon
        ttk.Label(
            self,
            text=icon,
            font=('Segoe UI', 48),
            background=parent["bg"]
        ).pack(pady=(50, 10))
        
        # Title
        ttk.Label(
            self,
            text=title,
            style="Title.TLabel"
        ).pack(pady=(0, 5))
        
        # Subtitle
        ttk.Label(
            self,
            text=subtitle,
            style="Subtitle.TLabel"
        ).pack()