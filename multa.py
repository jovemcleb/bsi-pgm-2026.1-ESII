def calcular_multa_com_carencia(dias_atraso, valor_dia, carencia=2):
    """Multa proporcional aos dias que excedem a carencia.

    Dentro da carencia, ou sem atraso, a multa e zero.
    Nunca retorna valor negativo.
    """
    dias_cobraveis = max(0, dias_atraso - carencia)
    return round(dias_cobraveis * valor_dia, 2)