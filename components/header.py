import tkinter as tk
from tkinter import ttk

class Header(tk.Frame):
    def __init__(self, parent, title, username=None, buttons=[]):
        super().__init__(parent, bg="#f8f9fa", padx=20, pady=10)
        self.pack(fill=tk.X)
        
        # Title label
        self.title_label = ttk.Label(
            self,
            text=title,
            style="Title.TLabel"
        )
        self.title_label.pack(side=tk.LEFT)
        
        # User info (if provided)
        if username:
            self.user_label = ttk.Label(
                self,
                text=f"Logged in as: {username}",
                style="Subtitle.TLabel"
            )
            self.user_label.pack(side=tk.LEFT, padx=10)
        
        # Button container
        self.button_frame = tk.Frame(self, bg="#f8f9fa")
        self.button_frame.pack(side=tk.RIGHT)
        
        # Add buttons
        for btn_text, btn_style, btn_command in buttons:
            ttk.Button(
                self.button_frame,
                text=btn_text,
                style=btn_style,
                command=btn_command
            ).pack(side=tk.LEFT, padx=5)