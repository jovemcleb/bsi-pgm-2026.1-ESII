import datetime
from typing import List, Optional

from negocio.models import Emprestimo
from negocio.repositories import RepositorioEmprestimo
from negocio.services.notificador import Notificador


class ServicoEmprestimo:
    def __init__(self, repositorio: RepositorioEmprestimo, notificador: Notificador):
        self.repositorio = repositorio
        self.notificador = notificador

    def registrar(self, equip_id: int, nome: str, email: str, dias: int) -> bool:
        ...

    def devolver(self, emprestimo_id: int) -> Optional[float]:
        ...

    def listar_atrasados(self) -> List[Emprestimo]:
        ...

    def calcular_atraso(self, data_devolucao: datetime.date) -> int:
        ...

    def calcular_multa(self, dias_atraso: int, tipo_equipamento: str) -> float:
        ...

    def verificar_atraso(self, data_devolucao: datetime.date) -> bool:
        ...