import tkinter as tk

from view.main_menu import MainMenu
from database.connection import initialize_database

def main():
    initialize_database()
    root = tk.Tk()

    MainMenu(root)

    root.mainloop()


if __name__ == "__main__":
    main()