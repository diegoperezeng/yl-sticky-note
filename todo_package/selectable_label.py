import tkinter as tk

class SelectableLabel(tk.Entry):
    def __init__(self, parent, text, custom_font, **kwargs):
        super().__init__(parent, **kwargs)
        self.insert(0, text)
        self.configure(state="readonly", readonlybackground="#FFD700", relief="flat", highlightthickness=0, font = custom_font)