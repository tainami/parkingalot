import os
from getpass import getpass

import requests

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:5000")

token = None


def requisicao(metodo, rota, dados=None, params=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    resposta = requests.request(
        metodo, f"{BASE_URL}{rota}", json=dados, params=params, headers=headers
    )

    print(f"\n[{resposta.status_code}]")
    if resposta.content:
        print(resposta.json())

    return resposta


def pedir(mensagem, obrigatorio=True):
    valor = input(mensagem).strip()
    while obrigatorio and not valor:
        valor = input(mensagem).strip()
    return valor


def pausar():
    input("\nPressione ENTER para continuar...")


# ---------- Login ----------


def login():
    global token

    cpf = pedir("CPF do guarda: ")
    senha = getpass("Senha: ")

    resposta = requisicao("POST", "/login/", {"cpf_guarda": cpf, "senha": senha})

    if resposta.status_code == 200:
        token = resposta.json()["token"]
        print("Login realizado.")

    pausar()


def logout():
    global token

    requisicao("POST", "/login/logout")
    token = None

    pausar()


# ---------- Colaboradores ----------


def listar_colaboradores():
    requisicao("GET", "/colaboradores/")
    pausar()


def buscar_colaborador():
    matricula = pedir("Matrícula: ")
    requisicao("GET", f"/colaboradores/{matricula}")
    pausar()


def cadastrar_colaborador():
    dados = {
        "matricula": int(pedir("Matrícula: ")),
        "nome": pedir("Nome: "),
        "setor": pedir("Setor: "),
        "cargo": pedir("Cargo: "),
    }
    requisicao("POST", "/colaboradores/", dados)
    pausar()


def editar_colaborador():
    matricula = pedir("Matrícula: ")
    dados = {}
    for campo in ["nome", "setor", "cargo"]:
        valor = pedir(f"{campo} (deixe vazio pra não alterar): ", obrigatorio=False)
        if valor:
            dados[campo] = valor
    requisicao("PUT", f"/colaboradores/{matricula}", dados)
    pausar()


def excluir_colaborador():
    matricula = pedir("Matrícula: ")
    requisicao("DELETE", f"/colaboradores/{matricula}")
    pausar()


def menu_colaboradores():
    while True:
        print("\n--- Colaboradores ---")
        print("1. Listar")
        print("2. Buscar por matrícula")
        print("3. Cadastrar")
        print("4. Editar")
        print("5. Excluir")
        print("0. Voltar")

        opcao = pedir("Escolha: ")

        if opcao == "1":
            listar_colaboradores()
        elif opcao == "2":
            buscar_colaborador()
        elif opcao == "3":
            cadastrar_colaborador()
        elif opcao == "4":
            editar_colaborador()
        elif opcao == "5":
            excluir_colaborador()
        elif opcao == "0":
            break


# ---------- Guardas ----------


def listar_guardas():
    requisicao("GET", "/guardas/")
    pausar()


def buscar_guarda():
    cpf = pedir("CPF: ")
    requisicao("GET", f"/guardas/{cpf}")
    pausar()


def cadastrar_guarda():
    dados = {
        "cpf_guarda": pedir("CPF: "),
        "nome_guarda": pedir("Nome: "),
        "turno": pedir("Turno: "),
        "senha": getpass("Senha: "),
    }
    requisicao("POST", "/guardas/", dados)
    pausar()


def editar_guarda():
    cpf = pedir("CPF: ")
    dados = {}
    for campo in ["nome_guarda", "turno"]:
        valor = pedir(f"{campo} (deixe vazio pra não alterar): ", obrigatorio=False)
        if valor:
            dados[campo] = valor

    senha = getpass("Nova senha (deixe vazio pra não alterar): ")
    if senha:
        dados["senha"] = senha

    requisicao("PUT", f"/guardas/{cpf}", dados)
    pausar()


def excluir_guarda():
    cpf = pedir("CPF: ")
    requisicao("DELETE", f"/guardas/{cpf}")
    pausar()


def menu_guardas():
    while True:
        print("\n--- Guardas ---")
        print("1. Listar")
        print("2. Buscar por CPF")
        print("3. Cadastrar")
        print("4. Editar")
        print("5. Excluir")
        print("0. Voltar")

        opcao = pedir("Escolha: ")

        if opcao == "1":
            listar_guardas()
        elif opcao == "2":
            buscar_guarda()
        elif opcao == "3":
            cadastrar_guarda()
        elif opcao == "4":
            editar_guarda()
        elif opcao == "5":
            excluir_guarda()
        elif opcao == "0":
            break


# ---------- Vagas ----------


def listar_vagas():
    requisicao("GET", "/vagas/")
    pausar()


def buscar_vaga():
    numero = pedir("Número da vaga: ")
    requisicao("GET", f"/vagas/{numero}")
    pausar()


def criar_vaga():
    dados = {
        "numero": int(pedir("Número: ")),
        "tipo_vaga": pedir("Tipo (COLABORADOR/TERCEIRO): "),
    }
    requisicao("POST", "/vagas/", dados)
    pausar()


def atualizar_vaga():
    numero = pedir("Número da vaga: ")
    tipo = pedir("Novo tipo (COLABORADOR/TERCEIRO): ")
    requisicao("PUT", f"/vagas/{numero}", {"tipo_vaga": tipo})
    pausar()


def menu_vagas():
    while True:
        print("\n--- Vagas ---")
        print("1. Listar")
        print("2. Buscar por número")
        print("3. Criar")
        print("4. Atualizar tipo")
        print("0. Voltar")

        opcao = pedir("Escolha: ")

        if opcao == "1":
            listar_vagas()
        elif opcao == "2":
            buscar_vaga()
        elif opcao == "3":
            criar_vaga()
        elif opcao == "4":
            atualizar_vaga()
        elif opcao == "0":
            break


# ---------- Veículos ----------


def listar_veiculos():
    matricula = pedir(
        "Filtrar por matrícula do colaborador (deixe vazio pra listar todos): ",
        obrigatorio=False,
    )
    params = {"matricula_colaborador": matricula} if matricula else None
    requisicao("GET", "/veiculos/", params=params)
    pausar()


def buscar_veiculo():
    placa = pedir("Placa: ")
    requisicao("GET", f"/veiculos/{placa}")
    pausar()


def cadastrar_veiculo():
    dados = {
        "placa": pedir("Placa: "),
        "modelo": pedir("Modelo: "),
        "cor": pedir("Cor: "),
        "tipo_veiculo": pedir("Tipo (CARRO/MOTO): "),
        "tipo_vinculo": pedir("Vínculo (COLABORADOR/TERCEIRO): "),
    }

    if dados["tipo_vinculo"] == "COLABORADOR":
        dados["matricula_colaborador"] = int(pedir("Matrícula do colaborador: "))
    else:
        dados["documento_responsavel"] = pedir("Documento do responsável: ")

    requisicao("POST", "/veiculos/", dados)
    pausar()


def editar_veiculo():
    placa = pedir("Placa: ")
    dados = {}
    for campo in ["modelo", "cor", "tipo_veiculo", "tipo_vinculo"]:
        valor = pedir(f"{campo} (deixe vazio pra não alterar): ", obrigatorio=False)
        if valor:
            dados[campo] = valor
    requisicao("PUT", f"/veiculos/{placa}", dados)
    pausar()


def excluir_veiculo():
    placa = pedir("Placa: ")
    requisicao("DELETE", f"/veiculos/{placa}")
    pausar()


def menu_veiculos():
    while True:
        print("\n--- Veículos ---")
        print("1. Listar (com filtro opcional por colaborador)")
        print("2. Buscar por placa")
        print("3. Cadastrar")
        print("4. Editar")
        print("5. Excluir")
        print("0. Voltar")

        opcao = pedir("Escolha: ")

        if opcao == "1":
            listar_veiculos()
        elif opcao == "2":
            buscar_veiculo()
        elif opcao == "3":
            cadastrar_veiculo()
        elif opcao == "4":
            editar_veiculo()
        elif opcao == "5":
            excluir_veiculo()
        elif opcao == "0":
            break


# ---------- Registros (entrada/saída) ----------


def listar_registros():
    data = pedir(
        "Filtrar por data (AAAA-MM-DD, deixe vazio pra ignorar): ", obrigatorio=False
    )
    placa = pedir("Filtrar por placa (deixe vazio pra ignorar): ", obrigatorio=False)

    params = {}
    if data:
        params["data"] = data
    if placa:
        params["placa"] = placa

    requisicao("GET", "/registros/", params=params or None)
    pausar()


def buscar_registro():
    id_registro = pedir("Id do registro: ")
    requisicao("GET", f"/registros/{id_registro}")
    pausar()


def registrar_entrada():
    dados = {
        "numero_vaga": int(pedir("Número da vaga: ")),
        "placa": pedir("Placa do veículo: "),
    }
    requisicao("POST", "/registros/", dados)
    pausar()


def registrar_saida():
    id_registro = pedir("Id do registro: ")
    requisicao("PUT", f"/registros/{id_registro}/saida")
    pausar()


def excluir_registro():
    id_registro = pedir("Id do registro: ")
    requisicao("DELETE", f"/registros/{id_registro}")
    pausar()


def menu_registros():
    while True:
        print("\n--- Registros de entrada/saída ---")
        print("1. Listar (com filtro opcional por data/placa)")
        print("2. Buscar por id")
        print("3. Registrar entrada")
        print("4. Registrar saída")
        print("5. Excluir")
        print("0. Voltar")

        opcao = pedir("Escolha: ")

        if opcao == "1":
            listar_registros()
        elif opcao == "2":
            buscar_registro()
        elif opcao == "3":
            registrar_entrada()
        elif opcao == "4":
            registrar_saida()
        elif opcao == "5":
            excluir_registro()
        elif opcao == "0":
            break


# ---------- Pagamentos ----------


def listar_pagamentos():
    requisicao("GET", "/pagamentos/")
    pausar()


def buscar_pagamento():
    id_pagamento = pedir("Id do pagamento: ")
    requisicao("GET", f"/pagamentos/{id_pagamento}")
    pausar()


def criar_pagamento():
    dados = {
        "id_registro": int(pedir("Id do registro: ")),
        "tipo_cartao": pedir("Tipo de cartão: "),
    }
    requisicao("POST", "/pagamentos/", dados)
    pausar()


def menu_pagamentos():
    while True:
        print("\n--- Pagamentos ---")
        print("1. Listar")
        print("2. Buscar por id")
        print("3. Criar (a partir de um registro com saída)")
        print("0. Voltar")

        opcao = pedir("Escolha: ")

        if opcao == "1":
            listar_pagamentos()
        elif opcao == "2":
            buscar_pagamento()
        elif opcao == "3":
            criar_pagamento()
        elif opcao == "0":
            break


# ---------- Menu principal ----------


def menu_principal():
    while True:
        opcoes = []

        if not token:
            opcoes.append(("Login", login))

        opcoes.append(("Colaboradores", menu_colaboradores))
        opcoes.append(("Guardas", menu_guardas))
        opcoes.append(("Vagas", menu_vagas))
        opcoes.append(("Veículos", menu_veiculos))
        opcoes.append(("Registros de entrada/saída", menu_registros))
        opcoes.append(("Pagamentos", menu_pagamentos))

        if token:
            opcoes.append(("Logout", logout))

        print("\n=== ParkingAlot ===")
        print(f"Logado: {'sim' if token else 'não'}")
        for numero, (nome, _) in enumerate(opcoes, start=1):
            print(f"{numero}. {nome}")
        print("0. Sair")

        opcao = pedir("Escolha: ")

        if opcao == "0":
            break

        try:
            _, funcao = opcoes[int(opcao) - 1]
            funcao()
        except (ValueError, IndexError):
            pass


if __name__ == "__main__":
    menu_principal()
