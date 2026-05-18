# Equipamento: contrato de multa por tipo de equipamento.
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Equipamento(ABC):
    id: int
    nome: str
    tipo: str
    disponivel: bool

    @abstractmethod
    def calcular_multa(self, dias_atraso: int) -> float:
        raise NotImplementedError


class Notebook(Equipamento):
    def __init__(self, id: int, nome: str, disponivel: bool):
        super().__init__(id=id, nome=nome, tipo="notebook", disponivel=disponivel)

    def calcular_multa(self, dias_atraso: int) -> float:
        return max(0, dias_atraso) * 10.0


class Projetor(Equipamento):
    def __init__(self, id: int, nome: str, disponivel: bool):
        super().__init__(id=id, nome=nome, tipo="projetor", disponivel=disponivel)

    def calcular_multa(self, dias_atraso: int) -> float:
        return max(0, dias_atraso) * 15.0


class CaboHDMI(Equipamento):
    def __init__(self, id: int, nome: str, disponivel: bool):
        super().__init__(id=id, nome=nome, tipo="cabo", disponivel=disponivel)

    def calcular_multa(self, dias_atraso: int) -> float:
        return max(0, dias_atraso) * 2.0
