import json
import os

class TodoItem:
    def __init__(self, text, checked):
        self.text = text
        self.checked = checked

class TodoListDB:
    def __init__(self, db_file):
        self.db_file = db_file

    def _convert_to_new_format(self, todo_list):
        new_format = []
        for item in todo_list:
            if isinstance(item, dict) and "item" in item and "checked" in item:
                new_format.append(item)
            else:
                new_format.append({"item": item, "checked": False})
        return new_format

    def get_todo_list(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                todo_list_data = json.load(f)
            return [TodoItem(item_data["text"], item_data["checked"]) for item_data in todo_list_data]
        else:
            return []

    def save_todo_list(self, todo_list):
        data = [{"text": item.text, "checked": item.checked} for item in todo_list]
        with open(self.db_file, 'w') as f:
            json.dump(data, f)