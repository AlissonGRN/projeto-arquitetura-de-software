from tkinter import ttk, messagebox


class ShoppingListView:
    def __init__(
        self,
        root,
        list_name="Lista de Compras"
    ):
        self.root = root
        self.list_name = list_name

        self.root.title(list_name)
        self.root.geometry("950x650")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(
            self.root,
            padding=25
        )

        main_frame.pack(
            expand=True,
            fill="both"
        )

        # -------------------------
        # Cabeçalho
        # -------------------------

        header_frame = ttk.Frame(
            main_frame
        )

        header_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        self.title_label = ttk.Label(
            header_frame,
            text=self.list_name,
            font=("Arial", 22, "bold")
        )

        self.title_label.pack(
            side="left"
        )

        self.back_button = ttk.Button(
            header_frame,
            text="Voltar para listas"
        )

        self.back_button.pack(
            side="right"
        )

        # -------------------------
        # Formulário
        # -------------------------

        form_frame = ttk.LabelFrame(
            main_frame,
            text="Adicionar produto",
            padding=15
        )

        form_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        # Produto
        product_label = ttk.Label(
            form_frame,
            text="Produto:"
        )

        product_label.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.product_entry = ttk.Entry(
            form_frame,
            width=30
        )

        self.product_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # Quantidade
        quantity_label = ttk.Label(
            form_frame,
            text="Quantidade:"
        )

        quantity_label.grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.quantity_entry = ttk.Entry(
            form_frame,
            width=12
        )

        self.quantity_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5,
            sticky="w"
        )

        # Categoria
        category_label = ttk.Label(
            form_frame,
            text="Categoria:"
        )

        category_label.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.category_entry = ttk.Entry(
            form_frame,
            width=30
        )

        self.category_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # Preço
        price_label = ttk.Label(
            form_frame,
            text="Preço unitário:"
        )

        price_label.grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.price_entry = ttk.Entry(
            form_frame,
            width=12
        )

        self.price_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.add_button = ttk.Button(
            form_frame,
            text="Adicionar produto"
        )

        self.add_button.grid(
            row=2,
            column=3,
            padx=5,
            pady=(15, 5),
            sticky="e"
        )

        # -------------------------
        # Tabela
        # -------------------------

        products_label = ttk.Label(
            main_frame,
            text="Produtos",
            font=("Arial", 14, "bold")
        )

        products_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        table_frame = ttk.Frame(
            main_frame
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        self.products_list = ttk.Treeview(
            table_frame,
            columns=(
                "product",
                "quantity",
                "category",
                "price",
                "subtotal"
            ),
            show="headings",
            height=12
        )

        self.products_list.heading(
            "product",
            text="Produto"
        )

        self.products_list.heading(
            "quantity",
            text="Qtd."
        )

        self.products_list.heading(
            "category",
            text="Categoria"
        )

        self.products_list.heading(
            "price",
            text="Preço unit."
        )

        self.products_list.heading(
            "subtotal",
            text="Subtotal"
        )

        self.products_list.column(
            "product",
            width=250
        )

        self.products_list.column(
            "quantity",
            width=70,
            anchor="center"
        )

        self.products_list.column(
            "category",
            width=180
        )

        self.products_list.column(
            "price",
            width=130,
            anchor="e"
        )

        self.products_list.column(
            "subtotal",
            width=130,
            anchor="e"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.products_list.yview
        )

        self.products_list.configure(
            yscrollcommand=scrollbar.set
        )

        self.products_list.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # -------------------------
        # Rodapé
        # -------------------------

        footer_frame = ttk.Frame(
            main_frame
        )

        footer_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        self.remove_button = ttk.Button(
            footer_frame,
            text="Excluir produto"
        )

        self.remove_button.pack(
            side="left"
        )

        totals_frame = ttk.Frame(
            footer_frame
        )

        totals_frame.pack(
            side="right"
        )

        self.items_total_label = ttk.Label(
            totals_frame,
            text="Total de itens: 0",
            font=("Arial", 11)
        )

        self.items_total_label.pack(
            anchor="e"
        )

        self.price_total_label = ttk.Label(
            totals_frame,
            text="Valor total: R$ 0,00",
            font=("Arial", 12, "bold")
        )

        self.price_total_label.pack(
            anchor="e",
            pady=(5, 0)
        )

    # =========================
    # Entrada
    # =========================

    def get_product_name(self):
        return self.product_entry.get()

    def get_quantity(self):
        return self.quantity_entry.get()

    def get_category(self):
        return self.category_entry.get()

    def get_price(self):
        return self.price_entry.get()

    def get_selected_item(self):
        selected = self.products_list.selection()

        if not selected:
            return None

        return selected[0]

    # =========================
    # Atualização
    # =========================

    def clear_inputs(self):
        self.product_entry.delete(
            0,
            "end"
        )

        self.quantity_entry.delete(
            0,
            "end"
        )

        self.category_entry.delete(
            0,
            "end"
        )

        self.price_entry.delete(
            0,
            "end"
        )

        self.product_entry.focus()

    def clear_products(self):
        for item in self.products_list.get_children():
            self.products_list.delete(item)

    def add_product_to_table(
        self,
        product_index,
        name,
        quantity,
        category,
        price
    ):
        subtotal = quantity * price

        self.products_list.insert(
            "",
            "end",
            iid=str(product_index),
            values=(
                name,
                quantity,
                category,
                self.format_currency(price),
                self.format_currency(subtotal)
            )
        )

    def update_items_total(self, total):
        self.items_total_label.config(
            text=f"Total de itens: {total}"
        )

    def update_price_total(self, total):
        self.price_total_label.config(
            text=f"Valor total: {self.format_currency(total)}"
        )

    # =========================
    # Eventos
    # =========================

    def set_add_command(self, command):
        self.add_button.config(
            command=command
        )

    def set_remove_command(self, command):
        self.remove_button.config(
            command=command
        )

    def set_back_command(self, command):
        self.back_button.config(
            command=command
        )

    # =========================
    # Mensagens
    # =========================

    def show_error(self, message):
        messagebox.showerror(
            "Erro",
            message
        )

    def confirm_delete_product(self, product_name):
        return messagebox.askyesno(
            "Excluir produto",
            f'Deseja realmente excluir "{product_name}"?'
        )

    # =========================
    # Formatação
    # =========================

    @staticmethod
    def format_currency(value_in_cents):
        value_in_cents = value_in_cents or 0

        value = value_in_cents / 100

        return (
            f"R$ {value:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )