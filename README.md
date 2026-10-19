# Projeto de Arquitetura de Software

Projeto acadêmico para demonstrar padrões de projeto em uma aplicação de listas de compras desenvolvida em Python com Tkinter.

## Padrões de projeto implementados

### Facade — Fachada

**Local:** `facade/shopping_facade.py`

A classe `ShoppingFacade` oferece uma interface simplificada para operações com listas de compras e produtos. A interface e os controladores podem usar essa fachada sem precisar coordenar diretamente todas as operações dos modelos.

### Singleton

**Local:** `facade/shopping_facade.py`

A classe `ShoppingFacade` também implementa o padrão Singleton. O método `__new__` cria a instância na primeira chamada e retorna essa mesma instância nas chamadas seguintes. O atributo `_initialized` impede que `__init__` reinicialize o estado compartilhado.

Assim, chamadas como:

```python
facade_a = ShoppingFacade()
facade_b = ShoppingFacade()

print(facade_a is facade_b)  # True
```

retornam referências ao mesmo objeto. As listas de compras e o contador de IDs são compartilhados durante a execução do programa.

### Observer — Observador

**Locais:** `observer/observer.py`, `models/shopping_list.py` e `controller/shopping_list_controller.py`

O modelo de lista de compras notifica os observadores registrados quando produtos são adicionados ou removidos, permitindo atualizar a interface sem acoplar o modelo diretamente à tela.

## Organização arquitetural

O projeto separa modelos (`models/`), interface gráfica (`view/`) e controladores (`controller/`), seguindo uma organização inspirada no MVC (Model-View-Controller).

## Observação

O Singleton mantém o estado apenas na memória do processo. Ele não substitui a persistência em banco de dados nem faz com que os dados sobrevivam ao encerramento do programa.
