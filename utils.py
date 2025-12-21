import tkinter as tk
import os
from tkinter import messagebox
from tkinter import simpledialog
#=========================================================================
# Error-Utilities

# Zentralisierte Fehlermeldungen
def show_error(graphic: bool=True, title: str="Error", text: str="An unknown error occurred."):
    print(f"⚠️ {title}: {text}\n")
    if graphic:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, text)
        root.destroy()

#=========================================================================
# CLI-Utilities

# Trennlinie im Terminal für saubere CLI-Abschnitte
def print_separation(length: int=50):
    print(f"\n{length*'='}")

# Mit Enter fortfahren
def enter_continue(msg: str="Press Enter to continue..."):
    input(f"\n{msg}")

# Leert das CLI komplett
def clear_cli():
    os.system('cls' if os.name == 'nt' else 'clear')

#=========================================================================
# Input-Utilities

# Um Integer abzufragen
def input_int(min_value: int=0, max_value: int=10000, default: int=100, msg: str="value", cli: bool=True) -> int:
    if cli:
        raw = input(f"{msg} (min: {min_value}, max: {max_value}): ").strip()
    else:
        root = tk.Tk()
        root.withdraw()
        raw = tk.simpledialog.askinteger("Input Value", f"Enter {msg}:", minvalue=min_value, maxvalue=max_value, initialvalue=default)
        root.destroy()

    if raw == '':
        return default

    try:
        value = int(raw)
    except ValueError:
        show_error(True, "Input Error", f"'{raw}' is not a valid integer.")
        return default

    if value > max_value:
        show_error(True, "Input Error", f"{value} is to big, maximal value is {max_value}.")
        return max_value
    
    elif value < min_value:
        show_error(True, "Input Error", f"{value} is to small, minimal value is {min_value}.")
        return min_value
    
    return value

def input_float(min_value: float=0, max_value: float=10000, default: float=100, msg: str="value", cli: bool=True) -> float:
    if cli:
        raw = input(f"{msg} (min: {min_value}, max: {max_value}): ").strip()
    else:
        root = tk.Tk()
        root.withdraw()
        raw = tk.simpledialog.askinteger("Input Value", f"Enter {msg}:", minvalue=min_value, maxvalue=max_value, initialvalue=default)
        root.destroy()

    if raw == '':
        return default

    try:
        value = float(raw)
    except ValueError:
        show_error(True, "Input Error", f"'{raw}' is not a valid Float.")
        return default

    if value > max_value:
        show_error(True, "Input Error", f"{value} is to big, maximal value is {max_value}.")
        return max_value
    
    elif value < min_value:
        show_error(True, "Input Error", f"{value} is to small, minimal value is {min_value}.")
        return min_value
    
    return value

# Um Strings abzufragen
def input_str(msg: str="value", cli: bool=True) -> str:
    if cli:
        value = input(f"{msg}: ").strip()
    else:
        root = tk.Tk()
        root.withdraw()
        # raw = tk.simpledialog.askstring("Input data", f"Enter {msg}:"initialvalue=default)
        root.destroy()

    if value == '':
        return None
    
    return value

# Ja/Nein Abfrage
def input_confirm(msg: str="Are you sure?", cli: bool=True) -> True:
    if cli:
        choice = input(f"{msg} (y/n): ").strip().lower()
        return choice == 'y'
    else:
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno("Confirm", msg)
        root.destroy()
        return result