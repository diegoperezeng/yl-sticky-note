import tkinter as tk

def show_error(message):
    error_window = tk.Toplevel()
    error_window.title("Error")
    error_window.geometry("300x100")
    error_label = tk.Label(error_window, text=message, wraplength=280, justify="center")
    error_label.pack(pady=10)
    error_button = tk.Button(error_window, text="OK", command=error_window.destroy)
    error_button.pack(pady=10)
