import tkinter as tk

from controller.app_controller import AppController
from database.connection import initialize_database


def main():
    initialize_database()

    root = tk.Tk()

    AppController(root)

    root.mainloop()


if __name__ == "__main__":
    main()