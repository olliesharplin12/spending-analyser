import os

def clear_terminal():
    """Clears the terminal window."""
    os.system("cls" if os.name == "nt" else "clear")
