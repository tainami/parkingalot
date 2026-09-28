from flask import Blueprint, jsonify, request

from app import db
from app.models.veiculo import Veiculo
from app.routes.login import autenticacao_obrigatoria
from app.validacao import campos_faltando

bp = Blueprint("veiculo", __name__, url_prefix="/veiculos")


@bp.route("/", methods=["GET"])
@autenticacao_obrigatoria
def listar():
    consulta = db.select(Veiculo)

    matricula_colaborador = request.args.get("matricula_colaborador")
    if matricula_colaborador:
        if not matricula_colaborador.isdigit():
            return jsonify({"error": "matricula_colaborador deve ser um número"}), 400

        consulta = consulta.where(
            Veiculo.matricula_colaborador == int(matricula_colaborador)
        )

    veiculos = db.session.execute(consulta).scalars()

    return jsonify([veiculo.to_dict() for veiculo in veiculos])


@bp.route("/<string:placa>", methods=["GET"])
@autenticacao_obrigatoria
def buscar(placa):
    veiculo = db.session.get(Veiculo, placa)

    if veiculo is None:
        return jsonify({"error": "Veículo não encontrado"}), 404

    return jsonify(veiculo.to_dict())


@bp.route("/", methods=["POST"])
@autenticacao_obrigatoria
def cadastrar():
    dados = request.get_json(silent=True) or {}

    matricula_colaborador = dados.get("matricula_colaborador")
    documento_responsavel = dados.get("documento_responsavel")
    tipo_vinculo = dados.get("tipo_vinculo")

    faltando = campos_faltando(dados, ["placa", "modelo", "cor", "tipo_veiculo"])
    if faltando:
        return jsonify(
            {"error": f"Campos obrigatórios faltando: {', '.join(faltando)}"}
        ), 400

    if tipo_vinculo not in ("COLABORADOR", "TERCEIRO"):
        return jsonify(
            {"error": "tipo_vinculo deve ser 'COLABORADOR' ou 'TERCEIRO'"}
        ), 400

    if tipo_vinculo == "COLABORADOR" and not matricula_colaborador:
        return jsonify({"error": "Informe a matrícula do colaborador"}), 400

    if tipo_vinculo == "TERCEIRO" and not documento_responsavel:
        return jsonify({"error": "Informe o documento do responsável"}), 400

    if db.session.get(Veiculo, dados["placa"]) is not None:
        return jsonify({"error": "Placa já cadastrada"}), 409

    veiculo = Veiculo(
        placa=dados["placa"],
        modelo=dados["modelo"],
        cor=dados["cor"],
        tipo_veiculo=dados["tipo_veiculo"],
        tipo_vinculo=dados["tipo_vinculo"],
        matricula_colaborador=matricula_colaborador,
        documento_responsavel=documento_responsavel,
    )

    db.session.add(veiculo)
    db.session.commit()

    return jsonify(veiculo.to_dict()), 201


@bp.route("/<string:placa>", methods=["PUT"])
@autenticacao_obrigatoria
def editar(placa):
    veiculo = db.session.get(Veiculo, placa)

    if veiculo is None:
        return jsonify({"error": "Veículo não encontrado"}), 404

    dados = request.get_json(silent=True) or {}

    if "tipo_vinculo" in dados and dados["tipo_vinculo"] not in (
        "COLABORADOR",
        "TERCEIRO",
    ):
        return jsonify(
            {"error": "tipo_vinculo deve ser 'COLABORADOR' ou 'TERCEIRO'"}
        ), 400

    campos_editaveis = [
        "modelo",
        "cor",
        "tipo_veiculo",
        "tipo_vinculo",
        "matricula_colaborador",
        "documento_responsavel",
    ]
    for campo in campos_editaveis:
        if campo in dados:
            setattr(veiculo, campo, dados[campo])

    db.session.commit()

    return jsonify(veiculo.to_dict())


@bp.route("/<string:placa>", methods=["DELETE"])
@autenticacao_obrigatoria
def deletar(placa):
    veiculo = db.session.get(Veiculo, placa)

    if veiculo is None:
        return jsonify({"error": "Veículo não encontrado"}), 404

    db.session.delete(veiculo)
    db.session.commit()

    return "", 204
