import tkinter as tk

from views.MainWindow import MainWindow
from controllers.MazeController import MazeController


def main() -> None:
    root = tk.Tk()

    view = MainWindow(root)
    controller = MazeController(view)

    root.mainloop()


if __name__ == "__main__":
    main()