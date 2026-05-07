import datetime
from typing import List, Optional

from negocio.models import Emprestimo, Equipamento


class RepositorioEmprestimo:
    def buscar_equipamento(self, equip_id: int) -> Optional[Equipamento]:
        ...

    def salvar_emprestimo(self, emprestimo: Emprestimo) -> None:
        ...

    def marcar_indisponivel(self, equip_id: int) -> None:
        ...

    def buscar_emprestimo(self, emprestimo_id: int) -> Optional[Emprestimo]:
        ...

    def registrar_devolucao(self, emprestimo_id: int, data_devolucao: datetime.date) -> None:
        ...

    def marcar_disponivel(self, equip_id: int) -> None:
        ...

    def listar_todos(self) -> List[Emprestimo]:
        ...
