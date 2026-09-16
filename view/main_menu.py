from tkinter import ttk, messagebox


class MainMenu:
    def __init__(
        self,
        root,
        on_create,
        on_open,
        on_delete
    ):
        self.root = root
        self.on_create = on_create
        self.on_open = on_open
        self.on_delete = on_delete

        self.root.title("Listas de Compras")
        self.root.geometry("750x520")
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

        # -------------------------
        # Cabeçalho
        # -------------------------

        title = ttk.Label(
            main_frame,
            text="Minhas Listas de Compras",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=(10, 5)
        )

        subtitle = ttk.Label(
            main_frame,
            text="Crie uma lista ou selecione uma existente para editar.",
            font=("Arial", 11)
        )

        subtitle.pack(
            pady=(0, 25)
        )

        # -------------------------
        # Criar lista
        # -------------------------

        create_frame = ttk.LabelFrame(
            main_frame,
            text="Nova lista",
            padding=15
        )

        create_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        name_label = ttk.Label(
            create_frame,
            text="Nome:"
        )

        name_label.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.name_entry = ttk.Entry(
            create_frame,
            width=45
        )

        self.name_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.create_button = ttk.Button(
            create_frame,
            text="Criar lista",
            command=self.on_create
        )

        self.create_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=5
        )

        # Permite criar apertando Enter
        self.name_entry.bind(
            "<Return>",
            lambda event: self.on_create()
        )

        # -------------------------
        # Listas
        # -------------------------

        list_label = ttk.Label(
            main_frame,
            text="Listas cadastradas",
            font=("Arial", 14, "bold")
        )

        list_label.pack(
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

        self.lists_table = ttk.Treeview(
            table_frame,
            columns=(
                "name",
                "items",
                "total"
            ),
            show="headings",
            height=11
        )

        self.lists_table.heading(
            "name",
            text="Nome"
        )

        self.lists_table.heading(
            "items",
            text="Itens"
        )

        self.lists_table.heading(
            "total",
            text="Valor total"
        )

        self.lists_table.column(
            "name",
            width=400
        )

        self.lists_table.column(
            "items",
            width=100,
            anchor="center"
        )

        self.lists_table.column(
            "total",
            width=150,
            anchor="e"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.lists_table.yview
        )

        self.lists_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.lists_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Duplo clique abre a lista
        self.lists_table.bind(
            "<Double-1>",
            lambda event: self.on_open()
        )

        # -------------------------
        # Botões
        # -------------------------

        actions_frame = ttk.Frame(
            main_frame
        )

        actions_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        self.open_button = ttk.Button(
            actions_frame,
            text="Abrir lista",
            command=self.on_open
        )

        self.open_button.pack(
            side="left"
        )

        self.delete_button = ttk.Button(
            actions_frame,
            text="Excluir lista",
            command=self.on_delete
        )

        self.delete_button.pack(
            side="right"
        )

    # =========================
    # Entrada
    # =========================

    def get_list_name(self):
        return self.name_entry.get()

    def get_selected_list_id(self):
        selected = self.lists_table.selection()

        if not selected:
            return None

        return int(selected[0])

    # =========================
    # Atualização
    # =========================

    def clear_name_input(self):
        self.name_entry.delete(
            0,
            "end"
        )

        self.name_entry.focus()

    def clear_lists(self):
        for item in self.lists_table.get_children():
            self.lists_table.delete(item)

    def add_list_to_table(
        self,
        list_id,
        name,
        items,
        total
    ):
        self.lists_table.insert(
            "",
            "end",
            iid=str(list_id),
            values=(
                name,
                items,
                self.format_currency(total)
            )
        )

    # =========================
    # Mensagens
    # =========================

    def show_error(self, message):
        messagebox.showerror(
            "Erro",
            message
        )

    def confirm_delete(self, list_name):
        return messagebox.askyesno(
            "Excluir lista",
            f'Deseja realmente excluir a lista "{list_name}"?'
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