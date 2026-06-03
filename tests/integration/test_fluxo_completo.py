from repositories.repositorio_emprestimo import RepositorioEmprestimo
from services.notificador import Notificador
from services.servico_emprestimo import ServicoEmprestimo


def test_fluxo_registrar_devolver_com_componentes_reais():
    # Arrange
    repositorio = RepositorioEmprestimo()
    notificador = Notificador()
    servico = ServicoEmprestimo(repositorio, notificador)

    # Act
    sucesso = servico.registrar(1, "Ana", "ana@ufra.edu.br", dias=7)
    emprestimo = repositorio.buscar_emprestimo(1)
    multa = servico.devolver(1)

    # Assert
    assert sucesso is True
    assert emprestimo is not None
    assert emprestimo.equipamento_id == 1
    assert emprestimo.devolvido is True
    assert multa == 0.0
    assert repositorio.buscar_equipamento(1).disponivel is True
