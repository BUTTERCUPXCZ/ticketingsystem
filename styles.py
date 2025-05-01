from tkinter import ttk

def configure_styles():
    """Configure custom styles for the application"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Colors
    primary_color = "#4f46e5"  # Indigo
    secondary_color = "#10b981"  # Emerald
    accent_color = "#f59e0b"  # Amber
    danger_color = "#ef4444"  # Red
    light_bg = "#f8f9fa"
    dark_bg = "#1e293b"
    text_color = "#334155"
    light_text = "#f8fafc"
    
    # General styles
    style.configure('.', background=light_bg, foreground=text_color)
    
    # Frame styles
    style.configure('Card.TFrame', background='white', relief='flat', 
                   borderwidth=0, bordercolor='#e2e8f0', padding=10)
    
    # Label styles
    style.configure('Header.TLabel', font=('Segoe UI', 24, 'bold'), 
                   foreground=primary_color, background=light_bg)
    style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), 
                   foreground=dark_bg, background=light_bg)
    style.configure('Subtitle.TLabel', font=('Segoe UI', 12), 
                   foreground='#64748b', background=light_bg)
    style.configure('FormLabel.TLabel', font=('Segoe UI', 11, 'bold'), 
                   foreground=text_color, background='white')
    style.configure('Footer.TLabel', font=('Segoe UI', 9), 
                   foreground='#64748b', background=light_bg)
    
    # Button styles
    style.configure('TButton', font=('Segoe UI', 10), padding=8)
    style.configure('Primary.TButton', foreground='white', background=primary_color)
    style.configure('Accent.TButton', foreground='white', background=accent_color)
    style.configure('Success.TButton', foreground='white', background=secondary_color)
    style.configure('Danger.TButton', foreground='white', background=danger_color)
    style.configure('Outline.TButton', foreground=primary_color, background='white',
                   bordercolor=primary_color, borderwidth=1)
    
    # Add hover effects for buttons
    style.map('Primary.TButton',
              background=[('active', '#4338ca')])
    style.map('Accent.TButton',
              background=[('active', '#d97706')])
    style.map('Success.TButton',
              background=[('active', '#0d9488')])
    style.map('Danger.TButton',
              background=[('active', '#dc2626')])
    style.map('Outline.TButton',
              background=[('active', '#eef2ff')])
    
    # Entry styles
    style.configure('FormEntry.TEntry', font=('Segoe UI', 11), 
                   fieldbackground='white', bordercolor='#cbd5e1',
                   relief='solid', borderwidth=1, padding=8)
    
    # Notebook styles
    style.configure('TNotebook', background=light_bg)
    style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), 
                   padding=[12, 4], background='#e2e8f0')
    style.map('TNotebook.Tab', 
              background=[('selected', 'white')],
              expand=[('selected', [1, 1, 1, 0])])
    
    # Treeview styles
    style.configure('Treeview', font=('Segoe UI', 10), rowheight=25)
    style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
    style.map('Treeview', background=[('selected', primary_color)])
    
    # Radio button styles
    style.configure('TRadiobutton', font=('Segoe UI', 10), background='white')
    
    # Scrollbar styles
    style.configure('Vertical.TScrollbar', arrowsize=15)