def campos_faltando(dados, campos_obrigatorios):
    return [campo for campo in campos_obrigatorios if not dados.get(campo)]
