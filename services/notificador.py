# Notificador: envio de mensagens de notificacao.
import datetime

from services.interfaces import INotificador


class Notificador(INotificador):
    def notificar_emprestimo(self, email: str, data_devolucao: datetime.date) -> None:
        print(f"[EMAIL] {email} — empréstimo até {data_devolucao}")

    def notificar_devolucao(self, email: str, multa: float) -> None:
        print(f"[EMAIL] {email} — multa R${multa:.2f}")

    def notificar_atraso(self, email: str, dias_atraso: int, multa: float) -> None:
        _ = dias_atraso, multa
        print(f"[EMAIL] {email} — você está em atraso!")
