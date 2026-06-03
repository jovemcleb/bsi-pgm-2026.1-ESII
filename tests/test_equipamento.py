import pytest

from models.equipamento import CaboHDMI, Notebook, Projetor


@pytest.mark.parametrize(
    "equipamento,dias,multa_esperada",
    [
        (Notebook(1, "Dell", True), 1, 10.0),
        (Notebook(1, "Dell", True), 3, 30.0),
        (Projetor(2, "Epson", True), 1, 15.0),
        (Projetor(2, "Epson", True), 2, 30.0),
        (CaboHDMI(3, "HDMI", True), 1, 2.0),
        (CaboHDMI(3, "HDMI", True), 5, 10.0),
    ],
)
def test_calcular_multa_atraso_positivo(equipamento, dias, multa_esperada):
    assert equipamento.calcular_multa(dias) == multa_esperada


@pytest.mark.parametrize(
    "equipamento",
    [
        Notebook(1, "Dell", True),
        Projetor(2, "Epson", True),
        CaboHDMI(3, "HDMI", True),
    ],
)
def test_calcular_multa_atraso_negativo_retorna_zero(equipamento):
    assert equipamento.calcular_multa(-3) == 0.0
