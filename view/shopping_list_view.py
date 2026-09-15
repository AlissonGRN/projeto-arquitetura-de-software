from tkinter import ttk, messagebox


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

        title.pack(
            pady=(10, 25)
        )

        form_frame = ttk.Frame(main_frame)

        form_frame.pack(
            fill="x",
            pady=(0, 20)
        )

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

        self.product_entry = ttk.Entry(
            form_frame,
            width=30
        )

        self.product_entry.grid(
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

        self.quantity_entry = ttk.Entry(
            form_frame,
            width=10
        )

        self.quantity_entry.grid(
            row=1,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        self.add_button = ttk.Button(
            form_frame,
            text="Adicionar"
        )

        self.add_button.grid(
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

        list_label.pack(
            anchor="w"
        )

        self.products_list = ttk.Treeview(
            main_frame,
            columns=("product", "quantity"),
            show="headings",
            height=8
        )

        self.products_list.heading(
            "product",
            text="Produto"
        )

        self.products_list.heading(
            "quantity",
            text="Quantidade"
        )

        self.products_list.column(
            "product",
            width=350
        )

        self.products_list.column(
            "quantity",
            width=120,
            anchor="center"
        )

        self.products_list.pack(
            fill="x",
            pady=10
        )

        self.remove_button = ttk.Button(
            main_frame,
            text="Remover"
        )

        self.remove_button.pack(
            anchor="e",
            pady=(5, 10)
        )

        self.total_label = ttk.Label(
            main_frame,
            text="Total de itens: 0",
            font=("Arial", 11, "bold")
        )

        self.total_label.pack(
            anchor="w",
            pady=10
        )

    def get_product_name(self):
        return self.product_entry.get()

    def get_quantity(self):
        return self.quantity_entry.get()

    def get_selected_item(self):
        selected = self.products_list.selection()

        if not selected:
            return None

        return selected[0]

    def clear_inputs(self):
        self.product_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")

        self.product_entry.focus()

    def clear_products(self):
        for item in self.products_list.get_children():
            self.products_list.delete(item)

    def add_product_to_table(self, product_index, name, quantity):
        self.products_list.insert(
            "",
            "end",
            iid=str(product_index),
            values=(name, quantity)
        )

    def update_total(self, total):
        self.total_label.config(
            text=f"Total de itens: {total}"
        )

    def set_add_command(self, command):
        self.add_button.config(
            command=command
        )

    def set_remove_command(self, command):
        self.remove_button.config(
            command=command
        )

    def show_error(self, message):
        messagebox.showerror(
            "Erro",
            message
        )

    def show_success(self, message):
        messagebox.showinfo(
            "Sucesso",
            message
        )