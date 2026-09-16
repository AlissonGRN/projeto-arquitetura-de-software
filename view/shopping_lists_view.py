from tkinter import ttk, messagebox


class ShoppingListsView:
    def __init__(self, root):
        self.root = root

        self.root.title("Minhas Listas")
        self.root.geometry("700x500")
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

        # Cabeçalho
        header_frame = ttk.Frame(main_frame)

        header_frame.pack(
            fill="x",
            pady=(0, 25)
        )

        title = ttk.Label(
            header_frame,
            text="Minhas Listas",
            font=("Arial", 22, "bold")
        )

        title.pack(
            side="left"
        )

        self.back_button = ttk.Button(
            header_frame,
            text="Voltar"
        )

        self.back_button.pack(
            side="right"
        )

        # Área de criação
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
            width=40
        )

        self.name_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.create_button = ttk.Button(
            create_frame,
            text="Criar lista"
        )

        self.create_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=5
        )

        # Listagem
        list_label = ttk.Label(
            main_frame,
            text="Listas cadastradas",
            font=("Arial", 14, "bold")
        )

        list_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        table_frame = ttk.Frame(main_frame)

        table_frame.pack(
            fill="both",
            expand=True
        )

        self.lists_table = ttk.Treeview(
            table_frame,
            columns=("name", "created_at"),
            show="headings",
            height=10
        )

        self.lists_table.heading(
            "name",
            text="Nome"
        )

        self.lists_table.heading(
            "created_at",
            text="Criada em"
        )

        self.lists_table.column(
            "name",
            width=380
        )

        self.lists_table.column(
            "created_at",
            width=180,
            anchor="center"
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

        # Botões inferiores
        actions_frame = ttk.Frame(main_frame)

        actions_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        self.open_button = ttk.Button(
            actions_frame,
            text="Abrir lista"
        )

        self.open_button.pack(
            side="left"
        )

        self.delete_button = ttk.Button(
            actions_frame,
            text="Excluir lista"
        )

        self.delete_button.pack(
            side="right"
        )

    # -------------------------
    # Entrada de dados
    # -------------------------

    def get_list_name(self):
        return self.name_entry.get()

    def get_selected_list(self):
        selected = self.lists_table.selection()

        if not selected:
            return None

        return selected[0]

    # -------------------------
    # Atualização da interface
    # -------------------------

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
        created_at=""
    ):
        self.lists_table.insert(
            "",
            "end",
            iid=str(list_id),
            values=(
                name,
                created_at
            )
        )

    # -------------------------
    # Eventos
    # -------------------------

    def set_create_command(self, command):
        self.create_button.config(
            command=command
        )

    def set_open_command(self, command):
        self.open_button.config(
            command=command
        )

    def set_delete_command(self, command):
        self.delete_button.config(
            command=command
        )

    def set_back_command(self, command):
        self.back_button.config(
            command=command
        )

    def set_double_click_command(self, command):
        self.lists_table.bind(
            "<Double-1>",
            command
        )

    # -------------------------
    # Mensagens
    # -------------------------

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

    def confirm_delete(self, list_name):
        return messagebox.askyesno(
            "Excluir lista",
            f'Deseja realmente excluir a lista "{list_name}"?'
        )