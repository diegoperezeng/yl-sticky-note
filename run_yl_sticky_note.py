import os
import sys
import todo_package
import src
import db_package

sys.path.append(os.path.abspath("src/"))
sys.path.append(os.path.abspath("db_package/"))
sys.path.append(os.path.abspath("todo_package/"))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.yl_sticky_note_main import TodoListApp

if __name__ == "__main__":
    app = TodoListApp()
    app.mainloop()