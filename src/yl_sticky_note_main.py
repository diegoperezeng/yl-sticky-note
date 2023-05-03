import tkinter as tk
from tkinter import ttk
from db_package.database import TodoListDB, TodoItem
from todo_package.todo_item_widget import TodoItemWidget
from todo_package.custom_title_bar import CustomTitleBar
from todo_package.resizable_window import ResizableWindow
import tkinter.font as tkFont
import json
import os
import sys



def create_database_file():
    packaged_db_path = get_resource_path('todolistdb.json')

    default_data = {
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
    
    if hasattr(sys, '_MEIPASS'):
        local_db_path = os.path.join(os.path.dirname(sys.executable), 'todolistdb.json')
    else:
        local_db_path = os.path.join(os.path.abspath('.'), 'todolistdb.json')
    
    if not os.path.exists(local_db_path):
        with open(local_db_path, 'w') as json_file:
            json.dump(default_data, json_file)
    
    return local_db_path


def show_error(title, message):
    error_window = tk.Toplevel()
    error_window.title(title)
    error_window.geometry("300x100")
    error_label = tk.Label(error_window, text=message, wraplength=280, justify="center")
    error_label.pack(pady=10)
    error_button = tk.Button(error_window, text="OK", command=error_window.destroy)
    error_button.pack(pady=10)

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

class TodoListApp(ResizableWindow):

    def update_entry_width(self, event):
        parent_width = event.width
        entry_width = parent_width - 10
        entry_chars = entry_width
        self.new_item_entry.config(width=entry_chars)
        # Add these lines to update the new item entry width when the window resizes
        if self.todo_list_widgets and hasattr(self, 'new_item_entry_id'):
            last_item_widget = self.todo_list_widgets[-1]
            y_pos = last_item_widget.winfo_y() + last_item_widget.winfo_height() + 5
            self.list_canvas.itemconfigure(self.new_item_entry_id, width=self.list_canvas.winfo_width() - self.scrollbar.winfo_width() - 10)

    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("To-Do List")
        self.attributes("-topmost", True)
        bg_color = "#FFD700"  # Set the desired background color
        self.configure(bg=bg_color)  # Change the background color to #FFD700
        
        #Access the database file
        try:
            db_file_path = create_database_file()
            self.db_file = TodoListDB(db_file_path)
        except Exception as e:
            show_error("Database Error", str(e))
            self.destroy()
            return

        self.custom_font = tkFont.Font(family = self.db_file.get_font_type(), size = self.db_file.get_font_size()) #Catch the app fonts config

        # Make the window resizable
        self.resizable(True, True)

        # Create Styles
        style = ttk.Style()
        style.theme_use("default")

        # Modify Styles
        style.configure("Custom.Vertical.TScrollbar",
            background="#FFD700",
            troughcolor="#FFEA99",
            gripcount=0,
            arrowsize=20)

        style.map("Custom.Vertical.TScrollbar",
            background=[("active", "#FFE066")],
            sliderrelief=[("pressed", "flat")],
            sliderborderwidth=[("pressed", 0)],
            sliderbackground=[("!disabled", "#FFD500")],
            slidersize=[("pressed", 20)],
            arrowcolor=[("pressed", "#FFB700"),
                        ("active", "#FFCB00"),
                        ("!disabled", "#FFD800")],
            troughcolor=[("!disabled", "#FFEA99")])

        
        
        

        self.todo_list, title, font_type, font_size = self.db_file.get_todo_list_title_and_font()        

        # Override the default title bar
        self.overrideredirect(True)
        self.custom_title_bar = CustomTitleBar(self,self.db_file,self.db_file.title,self.custom_font)

        self.custom_title_bar.title.delete(0, tk.END)
        self.custom_title_bar.title.insert(0, self.db_file.title)

        self.list_canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)  # Set the background color to #FFD700
        self.list_canvas.pack(fill="both", expand=True)
        self.list_frame = tk.Frame(self.list_canvas, bg=bg_color)
       
        self.scrollbar = ttk.Scrollbar(self.list_canvas, orient="vertical", command=self.list_canvas.yview, style="Custom.Vertical.TScrollbar")
        self.scrollbar.pack(side="right", fill="y")

        self.list_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.list_canvas.bind('<Configure>', lambda e: self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all")))

        self.list_canvas.create_window((0, 0), window=self.list_frame, anchor="nw", width=self.list_canvas.winfo_width() - self.scrollbar.winfo_width())


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
        self.new_item_entry.pack(pady=5, side="bottom", padx=5)

        self.bind("<Configure>", self.update_entry_width)        

        self.update_listbox()
        self.reposition_new_item_entry()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.update_idletasks()
        #self.minsize(self.winfo_width(), self.winfo_height())
        initial_event = tk.Event()
        initial_event.width = self.winfo_width()
        self.update_entry_width(initial_event)

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
        
         # If there's already an entry in the canvas, delete it
        if hasattr(self, 'new_item_entry_id'):
            self.list_canvas.delete(self.new_item_entry_id)
        
         # Create a new window item for the entry
        self.new_item_entry_id = self.list_canvas.create_window(
            5, y_pos, window=self.new_item_entry, anchor="nw",
            width=self.list_canvas.winfo_width() - self.scrollbar.winfo_width() - 10
        )
        
        #self.new_item_entry.place(in_=self.list_canvas, x=5, y=y_pos, relwidth=0.95)
        self.list_canvas.create_window(5, y_pos, window=self.new_item_entry, anchor="nw", width=self.list_canvas.winfo_width() - self.scrollbar.winfo_width() - 10)

    def update_listbox(self):
        selected_item = None
        
        if self.selected_item:
            selected_item = self.selected_item.item

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.todo_list_widgets = []

        for item in self.todo_list:
            item_widget = TodoItemWidget(self.list_frame, item, self.custom_font, self, self)
            item_widget.pack(fill="x")
            self.todo_list_widgets.append(item_widget)
            if item == selected_item:
                self.selected_item = item_widget
                item_widget.config(bg="lightblue")
                
        self.reposition_new_item_entry()

        self.list_frame.update_idletasks()
        self.list_canvas.config(scrollregion=self.list_canvas.bbox("all"))
    
    def toggle_strikethrough(self, index, var):
        if var.get():
            self.todo_list_widgets[index].config(font=("TkDefaultFont", 10, "overstrike"))
        else:
            self.todo_list_widgets[index].config(font=("TkDefaultFont", 10))

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
