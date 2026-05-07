import datetime


class Notificador:
    def notificar_emprestimo(self, email: str, data_devolucao: datetime.date) -> None:
        ...

    def notificar_devolucao(self, email: str, multa: float) -> None:
        ...

    def notificar_atraso(self, email: str, dias_atraso: int, multa: float) -> None:
        ...
