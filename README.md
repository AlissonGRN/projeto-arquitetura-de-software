# Lista de Compras

Aplicação desktop em Python e Tkinter para criar listas de compras, adicionar
produtos e acompanhar quantidades e valores totais. As listas e os produtos são
persistidos em SQLite, portanto continuam disponíveis após fechar e reabrir a
aplicação.

## Como executar

No Windows, com o ambiente virtual criado no projeto:

```powershell
.venv\Scripts\Activate.ps1
python main.py
```

O banco é criado automaticamente em `database/db.sqlite` na primeira execução.
A inicialização preserva os dados existentes e habilita a exclusão em cascata
dos produtos quando uma lista é removida.

## Testes

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes usam bancos temporários isolados e não alteram o banco da aplicação.

## DAOs

Os arquivos em `dao/` concentram o acesso ao SQLite:

- `ShoppingListDAO` cria, consulta e exclui listas.
- `ProductDAO` cria, consulta e exclui produtos.

A fachada continua sendo o ponto de acesso usado pelos controladores. Ela
carrega os dados persistidos ao ser inicializada e só atualiza o modelo e o
Observer depois que uma gravação ou exclusão no banco é concluída com sucesso.
