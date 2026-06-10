# ServicoEmprestimo: regras de negocio para emprestimos.
import datetime
from dataclasses import dataclass
from typing import List, Optional

from negocio.models import Emprestimo
from negocio.repositories import RepositorioEmprestimo
from negocio.services.notificador import Notificador


@dataclass
class ResumoAtraso:
    emprestimo: Emprestimo
    dias_atraso: int
    multa: float


class ServicoEmprestimo:
    def __init__(self, repositorio: RepositorioEmprestimo, notificador: Notificador):
        self.repositorio = repositorio
        self.notificador = notificador

    def registrar(self, equip_id: int, nome: str, email: str, dias: int) -> bool:
        emprestimos_do_usuario = 0
        for emprestimo in self.repositorio.listar_todos():
            if emprestimo.usuario_email == email:
                emprestimos_do_usuario += 1

        if emprestimos_do_usuario >= 2:
            return False

        equipamento = self.repositorio.buscar_equipamento(equip_id)
        if equipamento is None or not equipamento.disponivel:
            return False

        data_emprestimo = datetime.date.today()
        data_devolucao = data_emprestimo + datetime.timedelta(days=dias)
        emprestimo = Emprestimo(
            id=len(self.repositorio.listar_todos()) + 1,
            equipamento_id=equip_id,
            equipamento_nome=equipamento.nome,
            tipo=equipamento.tipo,
            usuario_nome=nome,
            usuario_email=email,
            data_emprestimo=data_emprestimo,
            data_devolucao=data_devolucao,
            devolvido=False,
        )

        self.repositorio.salvar_emprestimo(emprestimo)
        self.repositorio.marcar_indisponivel(equip_id)
        self.notificador.notificar_emprestimo(email, data_devolucao)
        return True

    def devolver(self, emprestimo_id: int) -> Optional[float]:
        emprestimo = self.repositorio.buscar_emprestimo(emprestimo_id)
        if emprestimo is None or emprestimo.devolvido:
            return None

        dias_atraso = self.calcular_atraso(emprestimo.data_devolucao)
        multa = self.calcular_multa(dias_atraso, emprestimo.equipamento_id)
        self.repositorio.registrar_devolucao(emprestimo_id, emprestimo.data_devolucao)
        self.repositorio.marcar_disponivel(emprestimo.equipamento_id)
        self.notificador.notificar_devolucao(emprestimo.usuario_email, multa)
        return multa

    def listar_atrasados(self) -> List[ResumoAtraso]:
        atrasados = []
        for emprestimo in self.repositorio.listar_todos():
            if emprestimo.devolvido:
                continue
            if self.verificar_atraso(emprestimo.data_devolucao):
                dias_atraso = self.calcular_atraso(emprestimo.data_devolucao)
                multa = self.calcular_multa(dias_atraso, emprestimo.equipamento_id)
                self.notificador.notificar_atraso(emprestimo.usuario_email, dias_atraso, multa)
                atrasados.append(
                    ResumoAtraso(
                        emprestimo=emprestimo,
                        dias_atraso=dias_atraso,
                        multa=multa,
                    )
                )
        return atrasados

    def calcular_atraso(self, data_devolucao: datetime.date) -> int:
        return (datetime.date.today() - data_devolucao).days

    def calcular_multa(self, dias_atraso: int, equipamento_id: int) -> float:
        equipamento = self.repositorio.buscar_equipamento(equipamento_id)
        if equipamento is None:
            return 0.0
        return equipamento.calcular_multa(dias_atraso)

    def verificar_atraso(self, data_devolucao: datetime.date) -> bool:
        return data_devolucao < datetime.date.today()