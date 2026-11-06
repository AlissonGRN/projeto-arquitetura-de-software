# Lista de Compras

Aplicação desktop em Python/Tkinter para criar listas de compras, cadastrar produtos e acompanhar quantidades e valores totais. Os dados ficam persistidos em SQLite.

O objetivo do projeto é demonstrar padrões de projeto de forma clara, com uma arquitetura pequena e organizada por responsabilidade.

## Como executar

Requisitos: Python 3.10 ou superior. Não há dependências externas.

    python main.py

O banco é criado automaticamente em `database/db.sqlite`.

## Estrutura do projeto

    main.py
    app/
    ├── bootstrap.py
    ├── domain/
    │   ├── money.py
    │   ├── product.py
    │   ├── shopping_list.py
    │   └── observer.py
    ├── application/
    │   ├── commands/
    │   │   ├── command.py
    │   │   ├── add_product_command.py
    │   │   ├── remove_product_command.py
    │   │   └── command_history.py
    │   ├── shopping_service.py
    │   ├── shopping_facade.py
    │   └── sorting.py
    ├── infrastructure/
    │   ├── database.py
    │   ├── schema.sql
    │   ├── product_dao.py
    │   └── shopping_list_dao.py
    └── presentation/
        ├── app_controller.py
        ├── shopping_list_controller.py
        ├── main_menu.py
        └── shopping_list_view.py

## Onde estão os padrões

- **MVC:** Views em `app/presentation/main_menu.py` e `shopping_list_view.py`; Controllers em `app/presentation/app_controller.py` e `shopping_list_controller.py`; entidades em `app/domain/`.
- **Value Object:** `app/domain/money.py` representa dinheiro em centavos, é imutável e valida os valores.
- **DAO:** `app/infrastructure/product_dao.py` e `shopping_list_dao.py` concentram o SQL. O ProductDAO converte `Money` para centavos na gravação e reconstrói o VO na leitura.
- **Facade:** `app/application/shopping_facade.py` é a entrada simples usada pelos Controllers e encaminha as operações ao ShoppingService.
- **Observer:** `ShoppingList` é o Subject; `ShoppingListController` é o Observer. O evento está em `app/domain/observer.py`.
- **Strategy:** `app/application/sorting.py` contém o contrato e as duas estratégias: ordenar por ID ou por nome.
- **Command:** `app/application/commands/` encapsula adicionar e remover produtos em comandos com `execute()` e `undo()`. `CommandHistory` mantém as pilhas de desfazer e refazer, usadas pelos botões **Desfazer** e **Refazer** da tela da lista.
- **Singleton:** `app/infrastructure/database.py` garante uma única instância do gerenciador SQLite. Cada operação abre e fecha sua própria conexão.

## Fluxo para adicionar um produto

1. A View coleta nome, quantidade, categoria e preço.
2. O Controller transforma o preço digitado em `Money`.
3. A Facade encaminha a solicitação para `ShoppingService`.
4. O serviço cria e valida `Product`, e chama `ProductDAO`.
5. O DAO grava os centavos no SQLite e retorna um Product com `Money` reconstruído.
6. O serviço adiciona o produto à `ShoppingList`.
7. A lista publica o evento Observer; o Controller recebe e atualiza a View.

A gravação ocorre antes da alteração em memória. Assim, uma falha no banco não atualiza a lista nem dispara o Observer.

## Decisão de escopo

As pastas representam partes compreensíveis do sistema, não padrões individuais. O projeto mantém separação suficiente para demonstrar arquitetura e padrões, sem adicionar várias camadas de abstração difíceis de justificar em uma atividade de disciplina.

O projeto não implementa Abstract Factory nesta versão.
