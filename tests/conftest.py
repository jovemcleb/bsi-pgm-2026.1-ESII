import datetime

import pytest

from models.equipamento import CaboHDMI, Notebook, Projetor
from repositories.interfaces import IRepositorioEmprestimo
from services.interfaces import INotificador
from services.servico_emprestimo import ServicoEmprestimo


# Fake: implementacao simplificada funcional em memoria.
class RepositorioFake(IRepositorioEmprestimo):
    def __init__(self):
        self._equipamentos = [
            Notebook(1, "Notebook Dell", True),
            Projetor(2, "Projetor Epson", True),
            CaboHDMI(3, "Cabo HDMI", True),
        ]
        self._emprestimos = []

    def buscar_equipamento(self, equip_id: int):
        return next((equipamento for equipamento in self._equipamentos if equipamento.id == equip_id), None)

    def salvar_emprestimo(self, emprestimo):
        self._emprestimos.append(emprestimo)

    def marcar_indisponivel(self, equip_id: int) -> None:
        equipamento = self.buscar_equipamento(equip_id)
        if equipamento is not None:
            equipamento.disponivel = False

    def buscar_emprestimo(self, emprestimo_id: int):
        return next((emprestimo for emprestimo in self._emprestimos if emprestimo.id == emprestimo_id), None)

    def registrar_devolucao(self, emprestimo_id: int, data_devolucao: datetime.date) -> None:
        _ = data_devolucao
        emprestimo = self.buscar_emprestimo(emprestimo_id)
        if emprestimo is not None:
            emprestimo.devolvido = True

    def marcar_disponivel(self, equip_id: int) -> None:
        equipamento = self.buscar_equipamento(equip_id)
        if equipamento is not None:
            equipamento.disponivel = True

    def listar_todos(self):
        return self._emprestimos


# Spy: registra chamadas para verificacao posterior.
class NotificadorSpy(INotificador):
    def __init__(self):
        self.eventos = []

    def notificar_emprestimo(self, email: str, data_devolucao: datetime.date) -> None:
        self.eventos.append(("emprestimo", email, data_devolucao))

    def notificar_devolucao(self, email: str, multa: float) -> None:
        self.eventos.append(("devolucao", email, multa))

    def notificar_atraso(self, email: str, dias_atraso: int, multa: float) -> None:
        self.eventos.append(("atraso", email, dias_atraso, multa))


@pytest.fixture
def repositorio_fake():
    return RepositorioFake()


@pytest.fixture
def notificador_spy():
    return NotificadorSpy()


@pytest.fixture
def servico(repositorio_fake, notificador_spy):
    return ServicoEmprestimo(repositorio_fake, notificador_spy)
