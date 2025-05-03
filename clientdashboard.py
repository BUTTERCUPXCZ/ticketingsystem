import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from components.header import Header
from components.ticket_card import TicketCard
from components.scrollable_frame import ScrollableFrame
from components.empty_state import EmptyState
from utils import load_data, save_data
from components.conversation_box import ConversationBox  # ✅ Now this will work
from utils import get_current_timestamp, get_new_ticket_id
from components.form import TicketForm


class ClientDashboard:
    def __init__(self, root, username, logout_callback):
        self.root = root
        self.username = username
        self.logout_callback = logout_callback

        self.create_widgets()
        self.show_my_tickets()

    def create_widgets(self):
        """Create client dashboard widgets"""
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Header with navigation
        Header(
            self.root,
            title="Client Dashboard",
            username=self.username,
            buttons=[
                ("My Tickets", "Outline.TButton", self.show_my_tickets),
                ("New Ticket", "Success.TButton", self.show_create_ticket),
                ("Logout", "Danger.TButton", self.handle_logout)
            ]
        )

        # Main content area
        self.main_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

    def handle_logout(self):
        """Handle logout action"""
        self.logout_callback()

    def show_my_tickets(self):
        """Show tickets created by the current user"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Add title
        ttk.Label(
            self.main_frame,
            text="My Tickets",
            style="Subtitle.TLabel"
        ).pack(anchor=tk.W, pady=(0, 10))

        # Create scrollable frame
        self.scroll_frame = ScrollableFrame(self.main_frame, bg="#f8f9fa")
        self.scroll_frame.pack(expand=True, fill=tk.BOTH)

        # Load and display tickets
        data = load_data()
        found = False

        for ticket_id, ticket in data["tickets"].items():
            if ticket["client"] == self.username:
                found = True
                TicketCard(
                    self.scroll_frame.scrollable_frame,
                    ticket_id,
                    ticket,
                    on_respond=self.respond_to_ticket,
                    show_conversation=self.show_conversation
                ).pack(fill=tk.X, padx=5, pady=5)

        if not found:
            EmptyState(
                self.scroll_frame.scrollable_frame,
                icon="📋",
                title="No Tickets Found",
                subtitle="You haven't created any tickets yet"
            ).pack(expand=True, fill=tk.BOTH, pady=50)

    def show_conversation(self, ticket_id):
        """Display full conversation for the ticket"""
        from components.conversation_box import ConversationBox

        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        data = load_data()
        ticket = data["tickets"].get(ticket_id)

        if not ticket:
            messagebox.showerror("Error", "Ticket not found")
            return

        convo_box = ConversationBox(
            parent=self.main_frame,
            ticket_id=ticket_id,
            conversation=ticket.get("conversation", []),
            back_callback=self.show_my_tickets  # Fixed this line
        )
        convo_box.pack(fill=tk.BOTH, expand=True)

    def respond_to_ticket(self, ticket_id, response_text):
        """Client responds to a ticket"""
        if not response_text.strip():
            messagebox.showwarning("Warning", "Response cannot be empty.")
            return False

        try:
            data = load_data()
            ticket = data["tickets"].get(ticket_id)

            if not ticket:
                messagebox.showerror("Error", "Ticket not found")
                return False

            if ticket["status"] == "Closed":
                messagebox.showerror("Error", "This ticket is already closed")
                return False

            # Initialize conversation if it doesn't exist
            if "conversation" not in ticket:
                ticket["conversation"] = [
                    {"sender": "client", "message": ticket["description"], "timestamp": str(
                        datetime.now())}
                ]

            ticket["conversation"].append({
                "sender": "client",
                "message": response_text,
                "timestamp": str(datetime.now())
            })

            save_data(data)
            self.show_conversation(ticket_id)
            return True

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save response: {str(e)}")
            return False

    def show_create_ticket(self):
        """Show create ticket form"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create container frame for better layout control
        container = ttk.Frame(self.main_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Add title
        ttk.Label(
            container,
            text="Create New Ticket",
            style="Subtitle.TLabel"
        ).pack(anchor=tk.W, pady=(0, 10))

        # Create TicketForm instance
        self.ticket_form = TicketForm(
            container,
            on_submit=self.save_ticket,
            on_cancel=self.show_my_tickets
        )
        self.ticket_form.pack(fill=tk.BOTH, expand=True, pady=10)

    def save_ticket(self, subject, description):
        """Save new ticket to database"""
        try:
            data = load_data()
            ticket_id = get_new_ticket_id(data)

            # Create new ticket structure
            new_ticket = {
                "subject": subject,
                "description": description,
                "client": self.username,
                "status": "Open",
                "conversation": [
                    {
                        "sender": "client",
                        "message": description,
                        "timestamp": get_current_timestamp()
                    }
                ]
            }

            # Validate required fields
            if not subject.strip() or not description.strip():
                messagebox.showwarning(
                    "Validation Error", "Subject and description are required")
                return

            data["tickets"][ticket_id] = new_ticket
            save_data(data)

            messagebox.showinfo(
                "Success",
                f"Ticket #{ticket_id} created successfully!\n"
                f"Subject: {subject}"
            )
            self.show_my_tickets()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create ticket: {str(e)}")
