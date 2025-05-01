import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from components.header import Header
from components.ticket_card import TicketCard
from components.scrollable_frame import ScrollableFrame
from components.empty_state import EmptyState
from components.form import ResponseForm, UserForm
from utils import load_data, save_data, get_current_timestamp

class AdminDashboard:
    def __init__(self, root, username, logout_callback):
        self.root = root
        self.username = username
        self.logout_callback = logout_callback
        
        # Configure styles
        self._configure_styles()
        
        self.create_widgets()
        self.show_all_tickets()
    
    def _configure_styles(self):
        """Configure custom styles for the dashboard"""
        style = ttk.Style()
        style.configure("Admin.TFrame", background="#e3f2fd", bordercolor="#bbdefb")
        style.configure("Client.TFrame", background="#f5f5f5", bordercolor="#e0e0e0")
        style.configure("Admin.TLabel", background="#e3f2fd", foreground="#0d47a1")
        style.configure("Client.TLabel", background="#f5f5f5", foreground="#4a148c")
    
    def create_widgets(self):
        """Create admin dashboard widgets"""
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header with navigation
        Header(
            self.root,
            title="Admin Dashboard",
            username=self.username,
            buttons=[
                ("All Tickets", "Outline.TButton", self.show_all_tickets),
                ("Create User", "Outline.TButton", self.show_create_user),
                ("Logout", "Danger.TButton", self.handle_logout)
            ]
        )
        
        # Main content area
        self.main_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

    def handle_logout(self):
        """Handle logout action"""
        self.logout_callback()
    
    def show_all_tickets(self):
        """Show all tickets in the system"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add title
        ttk.Label(
            self.main_frame,
            text="All Tickets",
            style="Subtitle.TLabel"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Create scrollable frame
        self.scroll_frame = ScrollableFrame(self.main_frame, bg="#f8f9fa")
        self.scroll_frame.pack(expand=True, fill=tk.BOTH)
        
        # Load and display tickets
        data = load_data()
        if not data["tickets"]:
            EmptyState(
                self.scroll_frame.scrollable_frame,
                icon="📭",
                title="No Tickets Found",
                subtitle="There are no tickets in the system yet"
            ).pack(expand=True, fill=tk.BOTH, pady=50)
        else:
            for ticket_id, ticket in data["tickets"].items():
                TicketCard(
                    self.scroll_frame.scrollable_frame,
                    ticket_id,
                    ticket,
                    admin=True,
                    on_respond=self.respond_to_ticket,
                    on_close=self.close_ticket
                ).pack(fill=tk.X, padx=5, pady=5)
    
    def respond_to_ticket(self, ticket_id, response_text=None):
        """Respond to a specific ticket with enhanced conversation view"""
        data = load_data()
        ticket = data["tickets"].get(ticket_id)
        
        if not ticket:
            messagebox.showerror("Error", "Ticket not found")
            return

        # Create response dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Ticket #{ticket_id} - Conversation")
        dialog.geometry("800x700")
        self.center_window(dialog)
        
        # Main container
        container = ttk.Frame(dialog)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Ticket info header
        info_frame = ttk.Frame(container)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text=f"Ticket #{ticket_id}", font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        ttk.Label(info_frame, text=f"Client: {ticket['client']}", font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=10)
        
        status_colors = {
            "Open": "#0369a1",
            "In Progress": "#92400e",
            "Closed": "#166534"
        }
        status_color = status_colors.get(ticket["status"], "#000000")
        
        status_label = ttk.Label(
            info_frame,
            text=f"Status: {ticket['status']}",
            font=('Segoe UI', 10, 'bold'),
            foreground=status_color
        )
        status_label.pack(side=tk.LEFT)
        
        # Conversation display
        conv_frame = ttk.Frame(container)
        conv_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable canvas for conversation
        canvas = tk.Canvas(conv_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(conv_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Display conversation messages
        if "conversation" in ticket:
            for msg in ticket["conversation"]:
                self._display_message(scrollable_frame, msg)
        
        # Response area
        response_frame = ttk.Frame(container)
        response_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(response_frame, text="Your Response:").pack(anchor=tk.W)
        response_entry = tk.Text(response_frame, height=5, font=('Segoe UI', 10))
        response_entry.pack(fill=tk.X, pady=5)
        
        if response_text:
            response_entry.insert("1.0", response_text)
        
        # Button frame
        button_frame = ttk.Frame(container)
        button_frame.pack(fill=tk.X)
        
        submit_btn = ttk.Button(
            button_frame,
            text="Send Response",
            style="Success.TButton",
            command=lambda: self._handle_admin_response(
                dialog, ticket_id, response_entry.get("1.0", tk.END).strip()
            )
        )
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        if ticket["status"] != "Closed":
            close_btn = ttk.Button(
                button_frame,
                text="Close Ticket",
                style="Danger.TButton",
                command=lambda: self._handle_close_ticket(dialog, ticket_id)
            )
            close_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        # Auto-scroll to bottom
        canvas.yview_moveto(1.0)
    
    def _display_message(self, parent, msg):
        """Display a single message in the conversation"""
        is_admin = msg["sender"] == "admin"
        bubble_frame = ttk.Frame(parent)
        bubble_frame.pack(fill=tk.X, pady=2, anchor=tk.E if is_admin else tk.W)
        
        # Message bubble
        bubble = ttk.Frame(
            bubble_frame,
            borderwidth=1,
            relief="solid",
            style="Admin.TFrame" if is_admin else "Client.TFrame"
        )
        bubble.pack(padx=5, ipadx=10, ipady=5)
        
        # Sender label
        sender = "You" if is_admin else "Client"
        ttk.Label(
            bubble,
            text=sender,
            font=('Segoe UI', 9, 'bold'),
            style="Admin.TLabel" if is_admin else "Client.TLabel"
        ).pack(anchor=tk.W)
        
        # Message content
        ttk.Label(
            bubble,
            text=msg["message"],
            font=('Segoe UI', 10),
            wraplength=600,
            style="Admin.TLabel" if is_admin else "Client.TLabel"
        ).pack(anchor=tk.W)
        
        # Timestamp
        ttk.Label(
            bubble,
            text=msg.get("timestamp", ""),
            font=('Segoe UI', 8),
            style="Admin.TLabel" if is_admin else "Client.TLabel"
        ).pack(anchor=tk.E)
    
    def _handle_admin_response(self, dialog, ticket_id, response_text):
        """Handle admin response submission"""
        if not response_text:
            messagebox.showwarning("Warning", "Response cannot be empty")
            return
        
        try:
            data = load_data()
            ticket = data["tickets"][ticket_id]
            
            # Add admin response to conversation
            ticket["conversation"].append({
                "sender": "admin",
                "message": response_text,
                "timestamp": get_current_timestamp()
            })
            
            # Update status if needed
            if ticket["status"] == "Open":
                ticket["status"] = "In Progress"
            
            save_data(data)
            dialog.destroy()
            self.show_all_tickets()
            messagebox.showinfo("Success", "Response sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send response: {str(e)}")
    
    def _handle_close_ticket(self, dialog, ticket_id):
        """Handle ticket closing from conversation view"""
        if messagebox.askyesno("Confirm", "Are you sure you want to close this ticket?"):
            self.close_ticket(ticket_id)
            dialog.destroy()
    
    def close_ticket(self, ticket_id):
        """Close a ticket officially"""
        try:
            data = load_data()
            data["tickets"][ticket_id]["status"] = "Closed"
            save_data(data)
            messagebox.showinfo("Success", f"Ticket #{ticket_id} has been closed!")
            self.show_all_tickets()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to close ticket: {str(e)}")
    
    def center_window(self, window):
        """Center a window on screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_create_user(self):
        """Show create user form"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add title
        ttk.Label(
            self.main_frame,
            text="Create New User",
            style="Subtitle.TLabel"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Create user form
        UserForm(
            self.main_frame,
            on_submit=self.save_user,
            on_cancel=self.show_all_tickets
        ).pack(fill=tk.X, padx=20, pady=10)
    
    def save_user(self, username, password, role):
        """Save new user to database"""
        try:
            data = load_data()
            
            if username in data["users"]:
                messagebox.showerror("Error", "User already exists")
                return
            
            data["users"][username] = {
                "password": password,
                "role": role
            }
            
            save_data(data)
            messagebox.showinfo("Success", f"User '{username}' created successfully!")
            self.show_all_tickets()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create user: {str(e)}")