import tkinter as tk
from todo_package.selectable_label import SelectableLabel
from db_package.database import TodoListDB, TodoItem

class TodoItemWidget(tk.Frame):
    def __init__(self, parent, item, app):
        super().__init__(parent)
        self.configure(bg="#FFD700")  # Set the background color to #FFD700

        self.app = app

        self.check_var = tk.BooleanVar(value=item.checked)
        self.check_var.trace_add("write", self.on_check_change)

        self.checkbox = tk.Checkbutton(self, variable=self.check_var, bg="#FFD700", activebackground="#FFD700")  # Set the background color to #FFD700
        self.checkbox.pack(side="left")

        self.label = SelectableLabel(self, item.text, bg="#FFD700")  # Set the background color to #FFD700
        self.label.pack(side="left", fill="x", expand=True)
        
        self.bind("<Button-1>", self.on_click)
        self.label.bind("<Button-1>", self.on_click)
        self.label.bind("<Double-Button-1>", self.on_double_click)
        self.label.bind("<Return>", self.on_return_key)
        self.checkbox.bind("<Button-1>", self.on_click_checkbox)

        self.item = item
    
    def on_double_click(self, event):
        self.label.config(state="normal")
        self.label.focus()
    
    def on_return_key(self, event):
        self.label.config(state="readonly")
        new_text = self.label.get()
        if new_text:
            self.item.text = new_text
            self.app.db_file.save_todo_list(self.app.todo_list)
        self.label.selection_clear()
    
    def on_check_change(self, *args):
        self.item.checked = self.check_var.get()
        self.app.db_file.save_todo_list(self.app.todo_list)

    def on_click(self, event):
        if self.app.selected_item and self.app.selected_item != self:
            self.app.selected_item.config(bg="#FFD700")
            self.app.selected_item.label.configure(readonlybackground="#FFD700", fg="black")

        if self.app.selected_item == self:
            self.config(bg="#FFD700")
            self.label.configure(readonlybackground="#FFD700", fg="black")
            self.app.selected_item = None
        else:
            self.app.selected_item = self
            self.config(bg="lightblue")
            self.label.configure(readonlybackground="lightblue", fg="black")
    
    def on_click_checkbox(self, event):
        if self.app.selected_item and self.app.selected_item != self:            
            self.app.selected_item.item.checked