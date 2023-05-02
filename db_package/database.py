import tkinter as tk
import os
import json


def show_error(title, message):
    error_window = tk.Toplevel()
    error_window.title(title)
    error_window.geometry("300x100")
    error_label = tk.Label(error_window, text=message, wraplength=280, justify="center")
    error_label.pack(pady=10)
    error_button = tk.Button(error_window, text="OK", command=error_window.destroy)
    error_button.pack(pady=10)

class TodoItem:
    def __init__(self, text, checked):
        self.text = text
        self.checked = checked

class TodoListDB:
    
    def __init__(self, db_file):
        self.db_file = db_file

        # Check if the file exists, if not create it with the desired structure
        if not os.path.exists(db_file):
            data = {
                "title": "List Title",
                "font_type": "Arial",
                "font_size": 20,    
                "todo_list": [
                    {
                        "text": "Example item 1",
                        "checked": False
                    }
                ]
            }
            with open(db_file, 'w') as f:
                json.dump(data, f)

        self.todo_list, self.title, self.font_type, self.font_size = self.get_todo_list_title_and_font()

    def get_todo_list_title_and_font(self):
        try:
            with open(self.db_file, "r") as file:
                data = json.load(file)
            todo_list = [TodoItem(item["text"], item["checked"]) for item in data.get("todo_list", [])]
            title = data.get("title", "To-Do List")
            font_type = data.get("font_type", "Arial")
            font_size = data.get("font_size", 20)
            return todo_list, title, font_type, font_size
        except (FileNotFoundError, json.JSONDecodeError):
            show_error("Error", "Unable to load the database file.")
            return [], "To-Do List on Error", "Arial", 20
    
    def get_font_type(self):
        return self.font_type

    def get_font_size(self):
        return self.font_size

    def save_font_type(self, font_type):
        try:
            with open(self.db_file, "r") as file:
                data = json.load(file)
            data["font_type"] = font_type
            with open(self.db_file, "w") as file:
                json.dump(data, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_font_size(self, font_size):
        try:
            with open(self.db_file, "r") as file:
                data = json.load(file)
            data["font_size"] = font_size
            with open(self.db_file, "w") as file:
                json.dump(data, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_todo_list(self, todo_list):
        try:
            with open(self.db_file, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"title": "To-Do List", "todo_list": []}
            
        data["todo_list"] = [{"text": item.text, "checked": item.checked} for item in todo_list]
        
        with open(self.db_file, "w") as file:
            json.dump(data, file, indent=4)  # Pretty-print the JSON with an indent of 4 spaces

    def save_title(self, title):
        try:
            with open(self.db_file, "r") as file:
                data = json.load(file)
            data["title"] = title
            with open(self.db_file, "w") as file:
                json.dump(data, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

