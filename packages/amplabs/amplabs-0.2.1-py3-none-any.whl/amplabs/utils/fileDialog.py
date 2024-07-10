import tkinter as tk
from tkinter import filedialog

def ask_directory():
    root = tk.Tk()
    root.attributes("-alpha", 0.0)
    root.attributes("-topmost", True)
    folder_path = filedialog.askdirectory()
    root.destroy()
    if not folder_path:
        return None
    return folder_path


if __name__ == "__main__":
    folder_path = ask_directory()
    if folder_path:
        print(folder_path)
    else:
        print("No folder selected")
