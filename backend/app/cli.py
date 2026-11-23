from datetime import datetime, timedelta
from decimal import Decimal

import click
from werkzeug.security import generate_password_hash

from app import db
from app.models.colaborador import Colaborador
from app.models.guarda import Guarda
from app.models.pagamento import Pagamento
from app.models.registro import Registro
from app.models.vaga import Vaga
from app.models.veiculo import Veiculo

TOTAL_VAGAS = 48

COLABORADORES = [
    (10482, "Marina Souza", "Financeiro", "Analista"),
    (10311, "Rafael Lima", "TI", "Desenvolvedor"),
    (10527, "Júlia Ramos", "RH", "Coordenadora"),
    (10190, "André Costa", "Comercial", "Vendedor"),
    (10604, "Bruno Teixeira", "Logística", "Supervisor"),
    (10255, "Camila Rocha", "Marketing", "Designer"),
    (10399, "Diego Martins", "TI", "Suporte"),
    (10078, "Fernanda Dias", "Jurídico", "Advogada"),
    (10466, "Gustavo Pires", "Operações", "Gerente"),
]

VEICULOS_COLABORADORES = [
    ("IXK4D21", "Fiat Argo", "Prata", 10482),
    ("JBR2F90", "VW Polo", "Branco", 10311),
    ("IVL3C77", "Chevrolet Onix", "Preto", 10527),
    ("MKD5E30", "Hyundai HB20", "Cinza", 10190),
    ("IZP6G02", "Jeep Renegade", "Verde", 10604),
    ("NFA4H81", "Honda Fit", "Azul", 10255),
    ("OBX7J49", "Fiat Mobi", "Branco", 10399),
    ("IAC9L15", "VW Gol", "Preto", 10078),
    ("SUV3M28", "Ford Ka", "Vermelho", 10466),
]

VEICULOS_TERCEIROS = [
    ("QHT8A14", "Renault Kwid", "Vermelho", "12341208"),
    ("RTA1B56", "Toyota Corolla", "Branco", "45620731"),
    ("PLM2K63", "Nissan Kicks", "Prata", "78988912"),
    ("HGT4R11", "Fiat Uno", "Branco", "31415926"),
]

ENTRADAS_EM_ABERTO = [
    (2, "IXK4D21", "07:42"),
    (6, "NFA4H81", "08:21"),
    (10, "JBR2F90", "07:55"),
    (11, "QHT8A14", "09:12"),
    (13, "OBX7J49", "08:34"),
    (15, "PLM2K63", "11:05"),
    (17, "IVL3C77", "08:03"),
    (18, "MKD5E30", "08:10"),
    (20, "RTA1B56", "10:26"),
    (21, "IAC9L15", "07:48"),
    (25, "IZP6G02", "07:30"),
    (31, "SUV3M28", "09:40"),
]

SAIDA_COM_PAGAMENTO = (34, "HGT4R11", "08:50", "10:48")


def hoje_as(hora):
    h, m = map(int, hora.split(":"))
    return datetime.now().replace(hour=h, minute=m, second=0, microsecond=0)


def calcular_valor(entrada, saida):
    tempo_cobrado = saida - entrada - timedelta(minutes=30)
    if tempo_cobrado <= timedelta(0):
        return Decimal("0.00")
    minutos = Decimal(str(tempo_cobrado.total_seconds() / 60))
    return (Decimal("3.00") / Decimal(60) * minutos).quantize(Decimal("0.01"))


def register_cli(app):
    @app.cli.command("criar-guarda")
    @click.option("--cpf", prompt=True)
    @click.option("--nome", prompt=True)
    @click.option("--turno", prompt=True)
    @click.option("--senha", prompt=True, hide_input=True, confirmation_prompt=True)
    def criar_guarda(cpf, nome, turno, senha):
        """Cria o primeiro guarda direto no banco, sem passar pela API."""
        if db.session.get(Guarda, cpf) is not None:
            click.echo("Já existe um guarda com esse CPF.")
            return

        guarda = Guarda(
            cpf_guarda=cpf,
            nome_guarda=nome,
            turno=turno,
            senha=generate_password_hash(senha),
        )
        db.session.add(guarda)
        db.session.commit()

        click.echo(f"Guarda '{nome}' criado com sucesso.")

    @app.cli.command("popular-banco")
    def popular_banco():
        """Cria vagas, colaboradores, veículos e registros de exemplo para desenvolvimento."""
        guarda = db.session.execute(db.select(Guarda)).scalars().first()
        if guarda is None:
            click.echo(
                "Nenhum guarda cadastrado. Rode antes: flask --app run criar-guarda"
            )
            return

        if db.session.execute(db.select(Vaga)).first() is not None:
            click.echo("O banco já tem vagas cadastradas. Nada foi alterado.")
            return

        ocupadas = {numero: placa for numero, placa, _ in ENTRADAS_EM_ABERTO}
        vinculo_por_placa = {
            placa: "COLABORADOR" for placa, *_ in VEICULOS_COLABORADORES
        }
        vinculo_por_placa |= {placa: "TERCEIRO" for placa, *_ in VEICULOS_TERCEIROS}

        for numero in range(1, TOTAL_VAGAS + 1):
            placa = ocupadas.get(numero)
            db.session.add(
                Vaga(
                    numero=numero,
                    tipo_vaga=vinculo_por_placa[placa] if placa else "COLABORADOR",
                    status_vaga=placa is not None,
                )
            )

        for matricula, nome, setor, cargo in COLABORADORES:
            db.session.add(
                Colaborador(matricula=matricula, nome=nome, setor=setor, cargo=cargo)
            )

        for placa, modelo, cor, matricula in VEICULOS_COLABORADORES:
            db.session.add(
                Veiculo(
                    placa=placa,
                    modelo=modelo,
                    cor=cor,
                    tipo_veiculo="CARRO",
                    tipo_vinculo="COLABORADOR",
                    matricula_colaborador=matricula,
                )
            )

        for placa, modelo, cor, documento in VEICULOS_TERCEIROS:
            db.session.add(
                Veiculo(
                    placa=placa,
                    modelo=modelo,
                    cor=cor,
                    tipo_veiculo="CARRO",
                    tipo_vinculo="TERCEIRO",
                    documento_responsavel=documento,
                )
            )

        db.session.flush()

        for numero, placa, hora in ENTRADAS_EM_ABERTO:
            db.session.add(
                Registro(
                    numero_vaga=numero,
                    placa=placa,
                    cpf_guarda=guarda.cpf_guarda,
                    data_entrada=hoje_as(hora),
                )
            )

        numero, placa, hora_entrada, hora_saida = SAIDA_COM_PAGAMENTO
        entrada, saida = hoje_as(hora_entrada), hoje_as(hora_saida)
        registro = Registro(
            numero_vaga=numero,
            placa=placa,
            cpf_guarda=guarda.cpf_guarda,
            data_entrada=entrada,
            data_saida=saida,
        )
        db.session.add(registro)
        db.session.flush()

        db.session.add(
            Pagamento(
                id_registro=registro.id_registro,
                valor=calcular_valor(entrada, saida),
                data_pagamento=saida.date(),
                hora_pagamento=saida.time(),
                tipo_cartao="Débito",
                status_pagamento=True,
            )
        )

        db.session.commit()

        click.echo(
            f"Banco populado: {TOTAL_VAGAS} vagas ({len(ENTRADAS_EM_ABERTO)} ocupadas), "
            f"{len(COLABORADORES)} colaboradores, "
            f"{len(VEICULOS_COLABORADORES) + len(VEICULOS_TERCEIROS)} veículos, "
            f"{len(ENTRADAS_EM_ABERTO) + 1} registros e 1 pagamento."
        )
