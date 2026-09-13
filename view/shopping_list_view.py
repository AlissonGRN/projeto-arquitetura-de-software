from tkinter import ttk


class ShoppingListView:
    def __init__(self, root):
        self.root = root

        self.root.title("Lista de Compras")
        self.root.geometry("650x500")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(
            self.root,
            padding=30
        )

        main_frame.pack(
            expand=True,
            fill="both"
        )

        title = ttk.Label(
            main_frame,
            text="Minha Lista de Compras",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=(10, 25))

        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill="x", pady=(0, 20))

        product_label = ttk.Label(
            form_frame,
            text="Produto:"
        )

        product_label.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        product_entry = ttk.Entry(
            form_frame,
            width=30
        )

        product_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        quantity_label = ttk.Label(
            form_frame,
            text="Quantidade:"
        )

        quantity_label.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        quantity_entry = ttk.Entry(
            form_frame,
            width=10
        )

        quantity_entry.grid(
            row=1,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        add_button = ttk.Button(
            form_frame,
            text="Adicionar"
        )

        add_button.grid(
            row=2,
            column=1,
            sticky="w",
            padx=5,
            pady=10
        )

        separator = ttk.Separator(
            main_frame,
            orient="horizontal"
        )

        separator.pack(
            fill="x",
            pady=15
        )

        list_label = ttk.Label(
            main_frame,
            text="Produtos",
            font=("Arial", 14, "bold")
        )

        list_label.pack(anchor="w")

        products_list = ttk.Treeview(
            main_frame,
            columns=("product", "quantity"),
            show="headings",
            height=8
        )

        products_list.heading(
            "product",
            text="Produto"
        )

        products_list.heading(
            "quantity",
            text="Quantidade"
        )

        products_list.column(
            "product",
            width=350
        )

        products_list.column(
            "quantity",
            width=120,
            anchor="center"
        )

        products_list.pack(
            fill="x",
            pady=10
        )

        remove_button = ttk.Button(
            main_frame,
            text="Remover"
        )

        remove_button.pack(
            anchor="e",
            pady=(5, 10)
        )

        total_label = ttk.Label(
            main_frame,
            text="Total de itens: 0",
            font=("Arial", 11, "bold")
        )

        total_label.pack(
            anchor="w",
            pady=10
        )