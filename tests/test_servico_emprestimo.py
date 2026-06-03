import datetime

import pytest


def test_registrar_devolve_true_quando_equipamento_disponivel(servico):
    # Arrange

    # Act
    registrado = servico.registrar(1, "Ana", "ana@x.com", 7)

    # Assert
    assert registrado is True


def test_registrar_devolve_false_quando_equipamento_indisponivel(servico, repositorio_fake):
    # Arrange
    repositorio_fake.buscar_equipamento(1).disponivel = False

    # Act
    registrado = servico.registrar(1, "Ana", "ana@x.com", 7)

    # Assert
    assert registrado is False


def test_registrar_notifica_usuario_apos_sucesso(servico, notificador_spy):
    # Arrange

    # Act
    servico.registrar(1, "Ana", "ana@x.com", 7)

    # Assert
    assert notificador_spy.eventos[0][0] == "emprestimo"
    assert notificador_spy.eventos[0][1] == "ana@x.com"


@pytest.mark.parametrize(
    "equipamento_id,dias_atraso,multa_esperada",
    [
        (1, 2, 20.0),
        (1, 5, 50.0),
        (2, 2, 30.0),
        (2, 5, 75.0),
        (3, 2, 4.0),
        (3, 5, 10.0),
    ],
)
def test_devolver_calcula_multa_correta_para_atraso(servico, repositorio_fake, equipamento_id, dias_atraso, multa_esperada):
    # Arrange
    servico.registrar(equipamento_id, "Ana", "ana@x.com", 7)
    emprestimo = repositorio_fake.buscar_emprestimo(1)
    emprestimo.data_devolucao = datetime.date.today() - datetime.timedelta(days=dias_atraso)

    # Act
    multa = servico.devolver(1)

    # Assert
    assert multa == multa_esperada


def test_devolver_marca_equipamento_como_disponivel(servico, repositorio_fake):
    # Arrange
    servico.registrar(1, "Ana", "ana@x.com", 7)
    emprestimo = repositorio_fake.buscar_emprestimo(1)
    emprestimo.data_devolucao = datetime.date.today() - datetime.timedelta(days=1)

    # Act
    servico.devolver(1)

    # Assert
    assert repositorio_fake.buscar_equipamento(1).disponivel is True


def test_devolver_falha_silenciosamente_para_emprestimo_inexistente(servico):
    # Arrange

    # Act
    multa = servico.devolver(999)

    # Assert
    assert multa is None
