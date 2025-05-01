import tkinter as tk
from tkinter import ttk, messagebox

class UserForm(ttk.Frame):
    def __init__(self, parent, on_submit=None, on_cancel=None):
        super().__init__(parent)
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create user form widgets"""
        # Form title
        ttk.Label(self, text="Create New User", style="Title.TLabel").pack(anchor=tk.W, pady=10)
        
        # Username field
        ttk.Label(self, text="Username:").pack(anchor=tk.W)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(fill=tk.X, pady=5)
        
        # Password field
        ttk.Label(self, text="Password:").pack(anchor=tk.W)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # Role selection
        ttk.Label(self, text="Role:").pack(anchor=tk.W)
        self.role_var = tk.StringVar(value="client")
        ttk.Radiobutton(
            self, 
            text="Admin", 
            variable=self.role_var, 
            value="admin"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            self, 
            text="Client", 
            variable=self.role_var, 
            value="client"
        ).pack(anchor=tk.W)
        
        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(
            button_frame,
            text="Create User",
            style="Success.TButton",
            command=self.handle_submit
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            style="Secondary.TButton",
            command=self.on_cancel
        ).pack(side=tk.RIGHT)
    
    def handle_submit(self):
        """Handle form submission"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showwarning("Validation Error", "Username and password are required")
            return
        
        if self.on_submit:
            self.on_submit(username, password, role)