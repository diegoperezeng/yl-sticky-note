import json

class TodoItem:
    def __init__(self, text, checked):
        self.text = text
        self.checked = checked

class TodoListDB:
    
    def __init__(self, db_file):
        self.db_file = db_file
        self.todo_list, self.title = self.get_todo_list_and_title()

    def get_todo_list_and_title(self):
        try:
            with open(self.db_file, "r") as file:
                data = json.load(file)
            todo_list = [TodoItem(item["text"], item["checked"]) for item in data.get("todo_list", [])]
            title = data.get("title", "To-Do List")
            return todo_list, title
        except (FileNotFoundError, json.JSONDecodeError):
             return [], "To-Do List on Error"

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

