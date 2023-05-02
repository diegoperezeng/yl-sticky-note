import tkinter as tk

class CustomTitleBar(tk.Frame):
    def __init__(self, parent, db,title, custom_font):
        super().__init__(parent)
        self.parent = parent
        bg_color = "#FFD700"  # Set the desired background color
        self.configure(bg=bg_color)
        self.pack(fill="x")
        self.db=db

        self.title = tk.Entry(self, relief="flat", justify="center", fg="black", readonlybackground=bg_color, insertbackground=bg_color, bd=0)

        if not title:  # Check if the title is empty
            title = "To-Do List"  # Use the hardcoded title if the provided title is empty

        self.title.insert(0, title)
        self.title.config(state="readonly", bg=bg_color, font=custom_font)
        self.title.pack(side="left", padx=80, fill="both", expand=True)

        close_button = tk.Button(self, text="X", bg=bg_color, command=self.parent.destroy, relief=tk.FLAT)
        close_button.pack(side="right")

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)

        self.title.bind("<Double-Button-1>", self.on_title_double_click)
        self.title.bind("<Return>", self.on_title_return)

    def on_click(self, event):
        self._drag_data = {"x": event.x_root, "y": event.y_root}

    def on_drag(self, event):
        delta_x = event.x_root - self._drag_data["x"]
        delta_y = event.y_root - self._drag_data["y"]

        self.parent.geometry(f"+{self.parent.winfo_x() + delta_x}+{self.parent.winfo_y() + delta_y}")

        self._drag_data["x"] = event.x_root
        self._drag_data["y"] = event.y_root
    
    def on_title_double_click(self, event):
        self.title.config(state="normal")
        self.title.focus()

    def on_title_return(self, event):
        self.title.config(state="readonly")
        new_title = self.title.get()
        self.db.save_title(new_title)