import tkinter as tk
from tkinter import ttk
from login import LoginScreen
from styles import configure_styles

class TicketingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticketing Service System")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        
        # Configure styles
        configure_styles()
        
        # Show login screen
        self.show_login_screen()
    
    def show_login_screen(self):
        """Show the login screen and clear any existing widgets"""
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create new login screen
        LoginScreen(self.root, self.on_login_success)
    
    def on_login_success(self, username, role):
        """Handle successful login"""
        from admindashboard import AdminDashboard
        from clientdashboard import ClientDashboard
        
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Show appropriate dashboard
        if role == "admin":
            AdminDashboard(self.root, username, self.show_login_screen)
        else:
            ClientDashboard(self.root, username, self.show_login_screen)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketingSystem(root)
    root.mainloop()