import datetime

from negocio.models.emprestimo import Emprestimo
from negocio.repositories import RepositorioEmprestimo
from negocio.services.servico_emprestimo import ServicoEmprestimo


class NotificadorFalso:
    def notificar_emprestimo(self, email, data_devolucao):
        _ = email, data_devolucao

    def notificar_devolucao(self, email, multa):
        _ = email, multa

    def notificar_atraso(self, email, dias_atraso, multa):
        _ = email, dias_atraso, multa


def adicionar_emprestimo(repositorio, emprestimo_id, equipamento_id, email, devolvido=False):
    equipamento = repositorio.buscar_equipamento(equipamento_id)
    hoje = datetime.date.today()
    repositorio.salvar_emprestimo(
        Emprestimo(
            id=emprestimo_id,
            equipamento_id=equipamento_id,
            equipamento_nome=equipamento.nome,
            tipo=equipamento.tipo,
            usuario_nome="Ana",
            usuario_email=email,
            data_emprestimo=hoje,
            data_devolucao=hoje + datetime.timedelta(days=3),
            devolvido=devolvido,
        )
    )
    if not devolvido:
        repositorio.marcar_indisponivel(equipamento_id)


def test_bloqueia_terceiro_emprestimo_em_aberto_do_mesmo_usuario():
    repositorio = RepositorioEmprestimo()
    servico = ServicoEmprestimo(repositorio, NotificadorFalso())
    adicionar_emprestimo(repositorio, 1, 1, "ana@email.com")
    adicionar_emprestimo(repositorio, 2, 2, "ana@email.com")

    registrado = servico.registrar(3, "Ana", "ana@email.com", 2)

    assert registrado is False