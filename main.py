import tkinter as tk

from controller.app_controller import AppController

from database.connection import initialize_database

from facade.shopping_facade import ShoppingFacade


def main():
    initialize_database()

    root = tk.Tk()

    facade = ShoppingFacade()

    AppController(
        root,
        facade
    )

    root.mainloop()


if __name__ == "__main__":
    main()