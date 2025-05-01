import tkinter as tk
from tkinter import ttk, messagebox

class ResponseForm(ttk.Frame):
    def __init__(self, parent, ticket_id, ticket_data, initial_response="", on_submit=None, on_close=None, on_cancel=None):
        super().__init__(parent)
        self.ticket_id = ticket_id
        self.ticket_data = ticket_data
        self.on_submit = on_submit
        self.on_close = on_close
        self.on_cancel = on_cancel
        
        # Set minimum window size
        self.master.minsize(500, 600)
        
        self.create_widgets(initial_response)
    
    def create_widgets(self, initial_response):
        # Ticket info
        ttk.Label(self, text=f"Ticket #{self.ticket_id}", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(self, text=f"From: {self.ticket_data['client']}", style="Subtitle.TLabel").pack(anchor=tk.W)
        ttk.Label(self, text=f"Status: {self.ticket_data['status']}", style="Subtitle.TLabel").pack(anchor=tk.W)
        
        # Conversation display
        conv_frame = ttk.Frame(self)
        conv_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(conv_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.conv_text = tk.Text(
            conv_frame, 
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            padx=10,
            pady=8,
            state=tk.DISABLED
        )
        self.conv_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.conv_text.yview)
        
        # Display conversation
        if "conversation" in self.ticket_data:
            for msg in self.ticket_data["conversation"]:
                sender = "Admin" if msg["sender"] == "admin" else "Client"
                self.conv_text.config(state=tk.NORMAL)
                self.conv_text.insert(tk.END, f"{sender}: {msg['message']}\n\n")
                self.conv_text.config(state=tk.DISABLED)
        
        # Response area
        response_frame = ttk.Frame(self)
        response_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(response_frame, text="Your Response:").pack(anchor=tk.W)
        self.response_entry = tk.Text(response_frame, height=4, font=('Segoe UI', 10))
        if initial_response:
            self.response_entry.insert("1.0", initial_response)
        self.response_entry.pack(fill=tk.X, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        button_frame.pack(fill=tk.X, pady=10)
        
        # Submit button (enabled or disabled based on status)
        self.submit_btn = ttk.Button(
            button_frame,
            text="Submit Response",
            style="Success.TButton",
            command=self.handle_submit
        )
        self.submit_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        if self.ticket_data["status"] in ["Closed", "Resolved"]:
            self.submit_btn.state(["disabled"])
        
        # Close button
        self.close_btn = ttk.Button(
            button_frame,
            text="Close Ticket",
            style="Danger.TButton",
            command=self.handle_close
        )
        self.close_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        if self.ticket_data["status"] in ["Closed", "Resolved"]:
            self.close_btn.state(["disabled"])
        
        # Cancel button
        ttk.Button(
            button_frame,
            text="Cancel",
            style="Secondary.TButton",
            command=self.on_cancel
        ).pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
    
    def handle_submit(self):
        """Handle response submission"""
        response_text = self.response_entry.get("1.0", tk.END).strip()
        
        if not response_text:
            messagebox.showwarning("Empty Response", "Please enter a response before submitting")
            return
        
        try:
            if self.on_submit:
                self.on_submit(self.ticket_id, response_text)
                messagebox.showinfo("Success", "Response submitted successfully!")
                self.master.destroy()  # Close the response window after submission
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit response: {str(e)}")
    
    def handle_close(self):
        """Handle ticket closing"""
        if messagebox.askyesno("Confirm", "Are you sure you want to close this ticket?"):
            if self.on_close:
                self.on_close(self.ticket_id)

class TicketForm(ttk.Frame):
    def __init__(self, parent, on_submit=None, on_cancel=None):
        super().__init__(parent)
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create ticket form widgets"""
        # Form title
        ttk.Label(self, text="Create New Ticket", style="Title.TLabel").pack(anchor=tk.W, pady=10)
        
        # Subject field
        ttk.Label(self, text="Subject:").pack(anchor=tk.W)
        self.subject_entry = ttk.Entry(self)
        self.subject_entry.pack(fill=tk.X, pady=5)
        
        # Description field
        ttk.Label(self, text="Description:").pack(anchor=tk.W)
        self.desc_entry = tk.Text(self, height=8, font=('Segoe UI', 10))
        self.desc_entry.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(
            button_frame,
            text="Create Ticket",
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
        subject = self.subject_entry.get().strip()
        description = self.desc_entry.get("1.0", tk.END).strip()
        
        if not subject or not description:
            messagebox.showwarning("Validation Error", "Subject and description are required")
            return
        
        if self.on_submit:
            self.on_submit(subject, description)


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