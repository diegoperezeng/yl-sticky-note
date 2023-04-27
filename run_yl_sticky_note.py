import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.yl_sticky_note_main import TodoListApp

if __name__ == "__main__":
    app = TodoListApp()
    app.mainloop()