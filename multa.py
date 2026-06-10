def calcular_multa_com_carencia(dias_atraso, valor_dia, carencia=2):
    if dias_atraso == 0:
        return 0.0

    return (dias_atraso - carencia) * valor_dia