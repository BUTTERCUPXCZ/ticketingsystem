import json
import os
from datetime import datetime

DATA_FILE = "data.json"

def load_data():
    """Load data from JSON file"""
    if not os.path.exists(DATA_FILE):
        # Initialize with empty database if file doesn't exist
        initial_data = {
            "users": {
                "admin": {
                    "password": "admin123",
                    "role": "admin"
                }
            },
            "tickets": {}
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(initial_data, f, indent=2)
        return initial_data
    
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_new_ticket_id(data):
    """Generate a new ticket ID"""
    existing_ids = [int(k) for k in data["tickets"].keys() if k.isdigit()]
    return str(max(existing_ids) + 1) if existing_ids else "1"

def get_current_timestamp():
    """Get current timestamp in readable format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")