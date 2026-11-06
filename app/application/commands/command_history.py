from app.application.commands.command import Command


class CommandHistory:
    """Gerencia as pilhas de undo e redo dos comandos executados."""

    def __init__(self):
        self._undo_stack: list[Command] = []
        self._redo_stack: list[Command] = []

    @property
    def can_undo(self):
        return bool(self._undo_stack)

    @property
    def can_redo(self):
        return bool(self._redo_stack)

    def execute(self, command: Command):
        # O comando entra no histórico antes da execução para que o
        # Observer já veja o estado correto ao atualizar a View.
        previous_redo = self._redo_stack
        self._undo_stack.append(command)
        # Uma nova operação invalida qualquer refazer pendente.
        self._redo_stack = []
        try:
            result = command.execute()
        except Exception:
            self._undo_stack.pop()
            self._redo_stack = previous_redo
            raise
        return result

    def undo(self):
        if not self._undo_stack:
            return False
        command = self._undo_stack.pop()
        self._redo_stack.append(command)
        try:
            command.undo()
        except Exception:
            # Mantém o comando no histórico caso o desfazer falhe.
            self._redo_stack.pop()
            self._undo_stack.append(command)
            raise
        return True

    def redo(self):
        if not self._redo_stack:
            return False
        command = self._redo_stack.pop()
        self._undo_stack.append(command)
        try:
            command.execute()
        except Exception:
            # Mantém o comando no histórico caso o refazer falhe.
            self._undo_stack.pop()
            self._redo_stack.append(command)
            raise
        return True
