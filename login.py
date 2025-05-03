import tkinter as tk
from tkinter import ttk, messagebox
from utils import load_data


class LoginScreen:
    def __init__(self, root, on_success_callback):
        self.root = root
        self.on_success = on_success_callback

        self.create_widgets()

    def create_widgets(self):
        """Create login screen widgets"""
        # Main container
        self.container = tk.Frame(self.root, bg="#f8f9fa")
        self.container.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)

        # Header
        self.header = ttk.Label(
            self.container,
            text="Ticketing Service System",
            style="Header.TLabel"
        )
        self.header.pack(pady=(0, 30))

        # Login card
        self.login_card = ttk.Frame(self.container, style="Card.TFrame")
        self.login_card.pack(pady=20, ipadx=30, ipady=30)

        # Username field
        ttk.Label(self.login_card, text="Username", style="FormLabel.TLabel").grid(
            row=0, column=0, padx=20, pady=(10, 5), sticky='w')
        self.username_entry = ttk.Entry(
            self.login_card,
            style="FormEntry.TEntry",
            font=('Segoe UI', 11)
        )
        self.username_entry.grid(
            row=1, column=0, padx=20, pady=(0, 15), ipadx=50)

        # Password field
        ttk.Label(self.login_card, text="Password", style="FormLabel.TLabel").grid(
            row=2, column=0, padx=20, pady=(5, 5), sticky='w')
        self.password_entry = ttk.Entry(
            self.login_card,
            show="•",
            style="FormEntry.TEntry",
            font=('Segoe UI', 11)
        )
        self.password_entry.grid(
            row=3, column=0, padx=20, pady=(0, 20), ipadx=50)

        # Login button
        self.login_btn = ttk.Button(
            self.login_card,
            text="Login",
            style="Accent.TButton",
            command=self.authenticate
        )
        self.login_btn.grid(row=4, column=0, pady=10, ipadx=30)

        # Footer
        self.footer = ttk.Label(
            self.container,
            text="© 2023 Ticketing System",
            style="Footer.TLabel"
        )
        self.footer.pack(side=tk.BOTTOM, pady=20)

        # Set focus to username field
        self.username_entry.focus()

        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.authenticate())

    def authenticate(self):
        """Authenticate user"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        data = load_data()

        if username in data["users"] and data["users"][username]["password"] == password:
            role = data["users"][username]["role"]
            self.on_success(username, role)
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password",
                parent=self.root
            )
