# app.py
import tkinter as tk
from src.controller.reverso_controller import ReversoController
from src.gui.reverso_app import ReversoApp

if __name__ == "__main__":
    root = tk.Tk()
    controller = ReversoController()
    app = ReversoApp(root, controller)
    root.mainloop()
