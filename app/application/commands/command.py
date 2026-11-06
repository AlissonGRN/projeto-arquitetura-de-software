from abc import ABC, abstractmethod


class Command(ABC):
    """Contrato comum para operações que podem ser desfeitas."""

    @abstractmethod
    def execute(self):
        """Executa a operação e devolve o resultado, quando houver."""
        raise NotImplementedError

    @abstractmethod
    def undo(self):
        """Desfaz a operação executada anteriormente."""
        raise NotImplementedError
