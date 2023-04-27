import tkinter as tk

class ResizableWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Enter>", self.update_cursor)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        if self.resize_flag:
            delta_x = event.x - self.start_x
            delta_y = event.y - self.start_y
            new_width = self.winfo_width() + delta_x
            new_height = self.winfo_height() + delta_y

            if new_width > self.winfo_reqwidth() and new_height > self.winfo_reqheight():
                self.geometry(f"{new_width}x{new_height}")
                self.start_x = event.x
                self.start_y = event.y

    def update_cursor(self, event):
        cursor = "arrow"
        if event.x > self.winfo_width() - 10 or event.y > self.winfo_height() - 10:
            cursor = "sizing"
        self.configure(cursor=cursor)
        self.resize_flag = cursor == "sizing"