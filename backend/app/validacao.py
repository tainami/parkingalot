def campos_faltando(dados, campos_obrigatorios):
    return [
        campo
        for campo in campos_obrigatorios
        if campo not in dados or dados[campo] is None
    ]
