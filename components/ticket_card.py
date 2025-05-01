import tkinter as tk
from tkinter import ttk
from datetime import datetime

class TicketCard(tk.Frame):
    def __init__(self, parent, ticket_id, ticket_data, admin=False, on_respond=None, on_close=None, show_conversation=None):
        super().__init__(parent, bg="white", bd=1, relief="solid", 
                         highlightbackground="#e2e8f0", padx=15, pady=15)
        
        self.ticket_id = ticket_id
        self.ticket_data = ticket_data
        self.admin = admin
        self.on_respond = on_respond
        self.on_close = on_close
        self.show_conversation = show_conversation
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create ticket card widgets"""
        # Header
        header_frame = tk.Frame(self, bg="white")
        header_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            header_frame,
            text=f"#{self.ticket_id}",
            bg="white",
            fg="#4f46e5",
            font=('Segoe UI', 12, 'bold')
        ).pack(side=tk.LEFT)

        status_bg = "#dcfce7" if self.ticket_data["status"] == "Closed" else \
                    "#fef3c7" if self.ticket_data["status"] == "In Progress" else "#e0f2fe"
        status_fg = "#166534" if self.ticket_data["status"] == "Closed" else \
                    "#92400e" if self.ticket_data["status"] == "In Progress" else "#0369a1"

        tk.Label(
            header_frame,
            text=self.ticket_data["status"].upper(),
            bg=status_bg,
            fg=status_fg,
            font=('Segoe UI', 9, 'bold'),
            padx=8,
            pady=2
        ).pack(side=tk.RIGHT)

        # Client info (admin view)
        if self.admin:
            client_frame = tk.Frame(self, bg="white")
            client_frame.pack(fill=tk.X, pady=(0, 8))
            tk.Label(client_frame, text="👤", bg="white", font=('Segoe UI', 10)).pack(side=tk.LEFT)
            tk.Label(client_frame, text=self.ticket_data["client"], bg="white", fg="#64748b", font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=5)

        # Subject
        tk.Label(
            self,
            text=self.ticket_data["subject"],
            bg="white",
            fg="#1e293b",
            font=('Segoe UI', 14, 'bold'),
            wraplength=700,
            justify=tk.LEFT
        ).pack(anchor='w', pady=(0, 10))

        # Show last 3 messages
        if "conversation" in self.ticket_data and self.ticket_data["conversation"]:
            conv_frame = tk.Frame(self, bg="white")
            conv_frame.pack(fill=tk.X, pady=(0, 10))

            tk.Label(conv_frame, text="Recent Messages:", bg="white", fg="#64748b", font=('Segoe UI', 10, 'bold')).pack(anchor='w')

            for msg in self.ticket_data["conversation"][-3:]: 
                msg_frame = tk.Frame(conv_frame, bg="white")
                msg_frame.pack(fill=tk.X, pady=2)

                sender = msg["sender"]
                sender_label = "You" if (sender == "client" and not self.admin) or (sender == "admin" and self.admin) else "Admin" if sender == "admin" else "Client"

                tk.Label(
                    msg_frame,
                    text=f"{sender_label}:",
                    bg="white",
                    fg="#4f46e5" if sender_label in ["You", "Admin"] else "#64748b",
                    font=('Segoe UI', 9, 'bold')
                ).pack(side=tk.LEFT)

                tk.Label(
                    msg_frame,
                    text=msg["message"],
                    bg="white",
                    fg="#334155",
                    font=('Segoe UI', 9),
                    wraplength=600,
                    justify=tk.LEFT
                ).pack(side=tk.LEFT, padx=5)

        # Action area
        action_frame = tk.Frame(self, bg="white")
        action_frame.pack(fill=tk.X, pady=(10, 0))

        # View conversation button
        if self.show_conversation:
            ttk.Button(
                action_frame,
                text="View Conversation",
                style="Outline.TButton",
                command=lambda: self.show_conversation(self.ticket_id)
            ).pack(side=tk.LEFT)

        # Actions based on admin/client and status
        if self.ticket_data["status"] != "Closed":
            if self.admin:
                if self.on_respond:
                    ttk.Button(
                        action_frame,
                        text="Respond",
                        style="Accent.TButton",
                        command=lambda: self.on_respond(self.ticket_id)
                    ).pack(side=tk.RIGHT, padx=5)

                if self.on_close:
                    ttk.Button(
                        action_frame,
                        text="Close Ticket",
                        style="Danger.TButton",
                        command=lambda: self.on_close(self.ticket_id)
                    ).pack(side=tk.RIGHT)
            else:
                self.response_entry = ttk.Entry(action_frame)
                self.response_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(10, 5))

                if self.on_respond:
                    ttk.Button(
                        action_frame,
                        text="Respond",
                        style="Accent.TButton",
                        command=self.handle_client_response
                    ).pack(side=tk.RIGHT)

    def handle_client_response(self):
        """Handle client response submission"""
        response_text = self.response_entry.get()
        if response_text.strip() and self.on_respond:
            self.on_respond(self.ticket_id, response_text)
