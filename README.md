# Lista de Compras

Aplicação desktop em Python/Tkinter para criar listas de compras, cadastrar produtos e acompanhar quantidades e valores totais. Os dados são persistidos em SQLite.

O foco do projeto é demonstrar padrões de projeto dentro de uma arquitetura organizada por responsabilidades, em vez de manter uma pasta para cada padrão.

## Executar

Requisitos: Python 3.10 ou superior. A aplicação usa apenas a biblioteca padrão do Python.

    python main.py

O banco é criado automaticamente em database/db.sqlite.

## Testes

    python -m unittest discover -s tests -v

Os testes usam bancos temporários; não modificam o banco usado pela aplicação.

## Arquitetura

    app/
    ├── domain/                 # regras e conceitos do negócio
    │   ├── entities/           # ShoppingList e Product
    │   ├── value_objects/      # Money (valor imutável em centavos)
    │   └── events/             # Observer e evento ShoppingListChanged
    ├── application/            # casos de uso e orquestração
    │   ├── services/            # ShoppingListService e ProductService
    │   ├── facades/             # ShoppingFacade
    │   ├── ports/               # contratos de repositório
    │   └── strategies/sorting/  # ordenação por ID ou nome
    ├── infrastructure/         # detalhes técnicos
    │   ├── database/            # Singleton Database e schema SQL
    │   └── persistence/sqlite/  # DAOs concretos do SQLite
    └── presentation/           # interface e fluxo de interação
        ├── controllers/         # Controllers MVC
        └── views/tkinter/       # telas Tkinter

    main.py                     # ponto de entrada

## Responsabilidades e padrões

- MVC: presentation/views/tkinter exibe a interface; presentation/controllers recebe ações, chama a Facade e atualiza as Views. As entidades do domínio não importam Tkinter.
- Value Object (VO): domain/value_objects/money.py representa dinheiro como centavos inteiros. É imutável, valida valores, executa soma/multiplicação e formata reais sem usar float para cálculos.
- DAO: infrastructure/persistence/sqlite concentra SQL. ProductDAO recebe uma entidade Product, grava unit_price.cents e reconstrói Money.from_cents(...) ao ler. O restante da aplicação não conhece nomes de colunas nem comandos SQL.
- Facade: application/facades/shopping_facade.py oferece operações simples para os Controllers. Ela não abre conexões, não executa SQL e não atualiza diretamente listas; delega aos serviços.
- Observer: ShoppingList é o Subject e mantém observadores. ShoppingListController implementa Observer. Após a persistência, a alteração no agregado dispara ShoppingListChanged, e o Controller redesenha a View. Ao voltar de uma lista, ele se desinscreve.
- Strategy: SortById e SortByName implementam SortingStrategy. O Controller escolhe a estratégia pela opção da interface; a Facade encaminha a política para ordenar o resultado sem duplicar algoritmo.
- Singleton: infrastructure/database/database.py garante uma única instância do gerenciador/configuração de banco na aplicação. Cada operação abre e fecha sua própria conexão SQLite; o Singleton não mantém uma conexão global compartilhada.

## Fluxo de inclusão de produto

1. A View coleta nome, quantidade, categoria e preço digitados.
2. ShoppingListController converte o preço para Money e chama ShoppingFacade.add_product(...).
3. A Facade delega a ProductService.
4. ProductService cria/valida Product, chama ProductDAO e aguarda a gravação.
5. ProductDAO grava os centavos no SQLite e retorna uma entidade reconstruída com Money.
6. Somente após sucesso, ProductService adiciona o produto ao agregado ShoppingList.
7. O agregado notifica ShoppingListController via Observer.
8. O Controller atualiza a View com preço unitário, subtotal e total.

Se a gravação falhar no passo 4/5, os passos 6/7 não acontecem: a lista em memória permanece consistente.

## Decisões de organização

- As pastas representam camadas e responsabilidades, não nomes de padrões.
- DAOs são detalhes de infraestrutura; VO e entidades pertencem ao domínio.
- A Facade não é Singleton. O gerenciamento de banco é Singleton e é montado no bootstrap.py.
- bootstrap.py é o composition root: instancia implementações concretas e injeta dependências. Isso evita que os Controllers construam DAOs ou conexões.
- ShoppingList é o agregado que protege as operações sobre os produtos e publica eventos de alteração.

O guia PDF de estudo acompanha a entrega e contém o mapa dos arquivos, o fluxo de execução e perguntas prováveis para a apresentação.
