import tkinter as tk
from tkinter import ttk

class ConversationBox(tk.Frame):
    def __init__(self, parent, ticket_id, conversation, back_callback):
        super().__init__(parent, bg="white", padx=20, pady=20)
        self.ticket_id = ticket_id
        self.conversation = conversation
        self.back_callback = back_callback
        self.create_widgets()

    def create_widgets(self):
        # Header
        tk.Label(
            self,
            text=f"Ticket #{self.ticket_id} - Conversation",
            font=('Segoe UI', 16, 'bold'),
            bg="white"
        ).pack(anchor="w", pady=(0, 10))

        # Scrollable conversation area
        container = tk.Frame(self, bg="white")
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))  # Added closing parenthesis here
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Display messages
        for msg in self.conversation:
            is_admin = msg["sender"] == "admin"
            msg_frame = tk.Frame(scrollable_frame, bg="white")
            msg_frame.pack(fill=tk.X, pady=5, anchor="e" if is_admin else "w")

            # Message bubble
            bubble = tk.Frame(
                msg_frame,
                bg="#e3f2fd" if is_admin else "#f5f5f5",
                padx=10,
                pady=5,
                relief="solid",
                borderwidth=1
            )
            bubble.pack()

            # Sender label
            tk.Label(
                bubble,
                text="Admin" if is_admin else "You",
                font=('Segoe UI', 9, 'bold'),
                fg="#0d47a1" if is_admin else "#4a148c",
                bg=bubble["bg"]
            ).pack(anchor="w")

            # Message content
            tk.Label(
                bubble,
                text=msg["message"],
                font=('Segoe UI', 10),
                wraplength=400,
                justify="left",
                bg=bubble["bg"]
            ).pack(anchor="w")

            # Timestamp
            tk.Label(
                bubble,
                text=msg["timestamp"],
                font=('Segoe UI', 8),
                fg="#616161",
                bg=bubble["bg"]
            ).pack(anchor="e")

        # Back button
        ttk.Button(
            self,
            text="Back to Tickets",
            command=self.back_callback
        ).pack(pady=(20, 0), anchor="e")