import tkinter as tk
from main_gui import GUI

class MainClass:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = GUI(self.root, self)
        self.root.mainloop()

if __name__ == "__main__":
    main = MainClass()
