import tkinter as tk

from views.MainWindow import MainWindow


def main() -> None:
    root = tk.Tk()

    MainWindow(root)

    root.mainloop()


if __name__ == "__main__":
    main()