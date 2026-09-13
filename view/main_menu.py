import tkinter as tk
from tkinter import ttk

from view.shopping_list_view import ShoppingListView


class MainMenu:
    def __init__(self, root):
        self.root = root

        self.root.title("Lista de Compras")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(
            self.root,
            padding=40
        )

        main_frame.pack(
            expand=True,
            fill="both"
        )

        title = ttk.Label(
            main_frame,
            text="Lista de Compras",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(40, 10))

        subtitle = ttk.Label(
            main_frame,
            text="Organize suas compras de forma simples.",
            font=("Arial", 11)
        )
        subtitle.pack(pady=(0, 40))

        start_button = ttk.Button(
            main_frame,
            text="Iniciar",
            command=self.start_application
        )

        start_button.pack(
            ipadx=30,
            ipady=8
        )

    def start_application(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ShoppingListView(self.root)