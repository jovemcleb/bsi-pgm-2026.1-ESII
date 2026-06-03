import datetime
from abc import ABC, abstractmethod


class INotificador(ABC):
    @abstractmethod
    def notificar_emprestimo(self, email: str, data_devolucao: datetime.date) -> None:
        raise NotImplementedError

    @abstractmethod
    def notificar_devolucao(self, email: str, multa: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def notificar_atraso(self, email: str, dias_atraso: int, multa: float) -> None:
        raise NotImplementedError
