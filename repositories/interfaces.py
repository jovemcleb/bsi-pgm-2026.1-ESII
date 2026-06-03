import datetime
from abc import ABC, abstractmethod
from typing import List, Optional

from models import Emprestimo, Equipamento


class IRepositorioEmprestimo(ABC):
    @abstractmethod
    def buscar_equipamento(self, equip_id: int) -> Optional[Equipamento]:
        raise NotImplementedError

    @abstractmethod
    def salvar_emprestimo(self, emprestimo: Emprestimo) -> None:
        raise NotImplementedError

    @abstractmethod
    def marcar_indisponivel(self, equip_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def buscar_emprestimo(self, emprestimo_id: int) -> Optional[Emprestimo]:
        raise NotImplementedError

    @abstractmethod
    def registrar_devolucao(self, emprestimo_id: int, data_devolucao: datetime.date) -> None:
        raise NotImplementedError

    @abstractmethod
    def marcar_disponivel(self, equip_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def listar_todos(self) -> List[Emprestimo]:
        raise NotImplementedError
