# RepositorioEmprestimo: persistencia em memoria para equipamentos, emprestimos.
import datetime
from typing import List, Optional

from negocio.models import Emprestimo, Equipamento


class RepositorioEmprestimo:
    def __init__(self):
        self.equipamentos = [
            Equipamento(id=1, nome="Notebook Dell", tipo="notebook", disponivel=True),
            Equipamento(id=2, nome="Projetor Epson", tipo="projetor", disponivel=True),
            Equipamento(id=3, nome="Cabo HDMI", tipo="cabo", disponivel=True),
        ]
        self.emprestimos_registrados: List[Emprestimo] = []

    def buscar_equipamento(self, equip_id: int) -> Optional[Equipamento]:
        for equipamento in self.equipamentos:
            if equipamento.id == equip_id:
                return equipamento
        return None

    def salvar_emprestimo(self, emprestimo: Emprestimo) -> None:
        self.emprestimos_registrados.append(emprestimo)

    def marcar_indisponivel(self, equip_id: int) -> None:
        equipamento = self.buscar_equipamento(equip_id)
        if equipamento is not None:
            equipamento.disponivel = False

    def buscar_emprestimo(self, emprestimo_id: int) -> Optional[Emprestimo]:
        for emprestimo in self.emprestimos_registrados:
            if emprestimo.id == emprestimo_id:
                return emprestimo
        return None

    def registrar_devolucao(self, emprestimo_id: int, data_devolucao: datetime.date) -> None:
        _ = data_devolucao
        emprestimo = self.buscar_emprestimo(emprestimo_id)
        if emprestimo is not None:
            emprestimo.devolvido = True

    def marcar_disponivel(self, equip_id: int) -> None:
        equipamento = self.buscar_equipamento(equip_id)
        if equipamento is not None:
            equipamento.disponivel = True

    def listar_todos(self) -> List[Emprestimo]:
        return self.emprestimos_registrados
