import tkinter as tk

from presentation.windows.main_window import MainWindow


def gui():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    gui()
