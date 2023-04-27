import tkinter as tk
from tkinter import ttk
from db_package.database import TodoListDB, TodoItem
from todo_package.todo_item_widget import TodoItemWidget
from todo_package.custom_title_bar import CustomTitleBar
from todo_package.resizable_window import ResizableWindow
import os


class TodoListApp(ResizableWindow):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("To-Do List")
        self.attributes("-topmost", True)
        bg_color = "#FFD700"  # Set the desired background color
        self.configure(bg=bg_color)  # Change the background color to #FFD700

        # Make the window resizable
        self.resizable(True, True)

        # Create Styles
        style = ttk.Style()
        style.configure("Custom.Vertical.TScrollbar", background=bg_color, troughcolor="yellow")


        # Override the default title bar
        self.overrideredirect(True)
        self.custom_title_bar = CustomTitleBar(self)

        db_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db_package', 'todolistdb.json')
        self.db_file = TodoListDB(db_file_path)

        self.todo_list, title = self.db_file.get_todo_list_and_title()
        self.custom_title_bar.title.delete(0, tk.END)
        self.custom_title_bar.title.insert(0, title)

        self.list_canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)  # Set the background color to #FFD700
        self.list_canvas.pack(fill="both", expand=True)
        self.list_frame = tk.Frame(self.list_canvas, bg=bg_color)
        self.list_canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        # self.scrollbar = tk.Scrollbar(self.list_canvas)
        # self.scrollbar.pack(side="right", fill="y")
        #(self, relief="flat", justify="center", fg="black", readonlybackground=bg_color, insertbackground=bg_color, bd=0)
        #self.scrollbar = tk.Scrollbar(self.list_canvas, orient="vertical", command=self.list_canvas.yview, activebackground=bg_color)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.list_canvas.yview, style="Custom.Vertical.TScrollbar")
        self.scrollbar.pack(side="right", fill="y")

        self.list_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.list_canvas.bind('<Configure>', lambda e: self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all")))


        self.todo_list_widgets = []

        self.selected_item = None
        
        # Create a frame for the buttons
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side="bottom", pady=(0, 5), anchor='w')

        self.add_button = tk.Button(self.buttons_frame, text="Add Item", command=self.add_item)
        self.add_button.pack(side="left")

        self.delete_button = tk.Button(self.buttons_frame, text="Delete Item", command=self.delete_item)
        self.delete_button.pack(side="left")

        self.new_item_entry = tk.Entry(self, bg="#E6BE8A")
        self.new_item_entry.pack(pady=5, side="bottom", fill="x", padx=5)        

        self.update_listbox()
        self.reposition_new_item_entry()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    def on_closing(self):
        self.db_file.save_todo_list(self.todo_list)
        self.selected_item = None
        self.destroy()

    def reposition_new_item_entry(self):
        self.list_frame.update_idletasks()
        if self.todo_list_widgets:
            last_item_widget = self.todo_list_widgets[-1]
            y_pos = last_item_widget.winfo_y() + last_item_widget.winfo_height() + 5
        else:
            y_pos = 5
        self.new_item_entry.place(in_=self.list_canvas, x=5, y=y_pos, relwidth=0.95)


    def update_listbox(self):
        selected_item = None
        
        if self.selected_item:
            selected_item = self.selected_item.item

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.todo_list_widgets = []

        for item in self.todo_list:
            item_widget = TodoItemWidget(self.list_frame, item, self)
            item_widget.pack(fill="x")
            self.todo_list_widgets.append(item_widget)
            if item == selected_item:
                self.selected_item = item_widget
                item_widget.config(bg="lightblue")
                
        self.reposition_new_item_entry()

        self.list_frame.update_idletasks()
        self.list_canvas.config(scrollregion=self.list_canvas.bbox("all"))


    def add_item(self):
        new_item = self.new_item_entry.get()
        if new_item:
            self.todo_list.append(TodoItem(new_item, False))
            self.db_file.save_todo_list(self.todo_list)
            self.update_listbox()
            self.reposition_new_item_entry()
            self.new_item_entry.delete(0, tk.END)
            self.selected_item = None

    def delete_item(self):
        if self.selected_item:
            index = self.todo_list.index(self.selected_item.item)
            del self.todo_list[index]
            self.db_file.save_todo_list(self.todo_list)
            self.update_listbox()
            self.reposition_new_item_entry()
            self.selected_item = None

    def edit_item(self):
        pass

    def on_closing(self):
        self.db_file.save_todo_list(self.todo_list)
        self.selected_item = None
        self.destroy()

if __name__ == "__main__":
    app = TodoListApp()
    app.mainloop()
