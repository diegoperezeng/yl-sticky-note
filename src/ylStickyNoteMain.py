import tkinter as tk
from database import TodoListDB, TodoItem


class TodoItemWidget(tk.Frame):
    def __init__(self, parent, item, app):
        super().__init__(parent)
        self.check_var = tk.BooleanVar(value=item.checked)
        self.check_var.trace_add("write", self.on_check_change)

        self.checkbox = tk.Checkbutton(self, variable=self.check_var)
        self.checkbox.pack(side="left")

        self.label = tk.Label(self, text=item.text)
        self.label.pack(side="left")

        self.app = app
        self.bind("<Button-1>", self.on_click)
        self.label.bind("<Button-1>", self.on_click)
        self.checkbox.bind("<Button-1>", self.on_click_checkbox)

        self.item = item
    
    def on_check_change(self, *args):
        self.item.checked = self.check_var.get()
        self.app.db.save_todo_list(self.app.todo_list)

    def on_click(self, event):
        if self.app.selected_item and self.app.selected_item != self:
            self.app.selected_item.config(bg="SystemButtonFace")
            self.app.selected_item.label.config(bg="SystemButtonFace", fg="black")

        if self.app.selected_item == self:
            self.config(bg="SystemButtonFace")
            self.label.config(bg="SystemButtonFace", fg="black")
            self.app.selected_item = None
        else:
            self.app.selected_item = self
            self.config(bg="lightblue")
            self.label.config(bg="lightblue", fg="black")
    
    def on_click_checkbox(self, event):
        if self.app.selected_item and self.app.selected_item != self:            
            self.app.selected_item.item.checked

class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("To-Do List")

        self.db = TodoListDB("./db/todolistdb.txt")
        self.todo_list = self.db.get_todo_list()

        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.todo_list_widgets = []

        self.selected_item = None

        self.update_listbox()

        # Create a frame for the buttons
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side="bottom", pady=(0, 5), anchor='w')

        self.add_button = tk.Button(self.buttons_frame, text="Add Item", command=self.add_item)
        self.add_button.pack(side="left")

        self.delete_button = tk.Button(self.buttons_frame, text="Delete Item", command=self.delete_item)
        self.delete_button.pack(side="left")

        self.edit_button = tk.Button(self.buttons_frame, text="Edit Item", command=self.edit_item)
        self.edit_button.pack(side="left")

        self.new_item_entry = tk.Entry(self)
        self.new_item_entry.pack(pady=5, side="bottom", fill="x", padx=5)        

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.db.save_todo_list(self.todo_list)
        self.selected_item = None
        self.destroy()

    def update_listbox(self):
        selected_item = None
        
        if self.selected_item:
            selected_item = self.selected_item.item

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for item in self.todo_list:
            item_widget = TodoItemWidget(self.list_frame, item, self)
            item_widget.pack(fill="x")
            if item == selected_item:
                self.selected_item = item_widget
                item_widget.config(bg="lightblue")

    def add_item(self):
        new_item = self.new_item_entry.get()
        if new_item:
            self.todo_list.append(TodoItem(new_item, False))
            self.db.save_todo_list(self.todo_list)
            self.update_listbox()
            self.new_item_entry.delete(0, tk.END)
            self.selected_item = None

    def delete_item(self):
        if self.selected_item:
            index = self.todo_list.index(self.selected_item.item)
            del self.todo_list[index]
            self.db.save_todo_list(self.todo_list)
            self.update_listbox()
            self.selected_item = None

    def edit_item(self):
        if self.selected_item:
            index = self.todo_list.index(self.selected_item.item)
            item = self.todo_list[index]

            edit_window = tk.Toplevel(self)
            edit_window.title("Edit Item")
            edit_window.geometry("200x100")
            edit_window.transient(self)

            edit_entry = tk.Entry(edit_window)
            edit_entry.insert(0, item.text)
            edit_entry.pack()

            def save_changes():
                new_item = edit_entry.get()
                if new_item:
                    self.todo_list[index].text = new_item
                    self.db.save_todo_list(self.todo_list)
                    self.update_listbox()
                    edit_window.destroy()

            save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
            save_button.pack()
            self.selected_item = None

    def on_closing(self):
        self.db.save_todo_list(self.todo_list)
        self.selected_item = None
        self.destroy()

if __name__ == "__main__":
    app = TodoListApp()
    app.mainloop()
