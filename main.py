import tkinter as tk

from view.main_menu import MainMenu


def main():
    root = tk.Tk()

    MainMenu(root)

    root.mainloop()


if __name__ == "__main__":
    main()