"""TODO list do kata de multa com carencia.

- atraso 0 dias -> multa 0,00
- atraso alem da carencia -> cobra os dias excedentes
- atraso dentro da carencia -> multa 0,00
- valor por dia configuravel
- arredondar para 2 casas
"""

from multa import calcular_multa_com_carencia


def test_sem_atraso_nao_gera_multa():
    multa = calcular_multa_com_carencia(dias_atraso=0, valor_dia=10.0)

    assert multa == 0.0


def test_cobra_dias_excedentes_alem_da_carencia():
    multa = calcular_multa_com_carencia(dias_atraso=5, valor_dia=10.0, carencia=2)

    assert multa == 30.0