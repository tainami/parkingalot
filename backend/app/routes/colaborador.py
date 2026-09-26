from flask import Blueprint, jsonify, request

from app import db
from app.models.colaborador import Colaborador
from app.routes.login import verificar_token

bp = Blueprint("colaborador", __name__, url_prefix="/colaboradores")


@bp.route("/", methods=["GET"])
def listar():
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    colaboradores = db.session.execute(db.select(Colaborador)).scalars()

    return jsonify([colaborador.to_dict() for colaborador in colaboradores])


@bp.route("/<int:matricula>", methods=["GET"])
def buscar(matricula):
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    colaborador = db.session.get(Colaborador, matricula)

    if colaborador is None:
        return jsonify({"error": "Colaborador não encontrado"}), 404

    return jsonify(colaborador.to_dict())


@bp.route("/", methods=["POST"])
def cadastrar():
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    dados = request.get_json(silent=True) or {}

    campos_obrigatorios = ["matricula", "nome", "setor", "cargo"]
    faltando = [campo for campo in campos_obrigatorios if not dados.get(campo)]
    if faltando:
        return jsonify(
            {"error": f"Campos obrigatórios faltando: {', '.join(faltando)}"}
        ), 400

    if db.session.get(Colaborador, dados["matricula"]) is not None:
        return jsonify({"error": "Matrícula já cadastrada"}), 409

    colaborador = Colaborador(
        matricula=dados["matricula"],
        nome=dados["nome"],
        setor=dados["setor"],
        cargo=dados["cargo"],
    )
    db.session.add(colaborador)
    db.session.commit()

    return jsonify(colaborador.to_dict()), 201


@bp.route("/<int:matricula>", methods=["PUT"])
def editar(matricula):
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    colaborador = db.session.get(Colaborador, matricula)

    if colaborador is None:
        return jsonify({"error": "Colaborador não encontrado"}), 404

    dados = request.get_json(silent=True) or {}
    for campo in ["nome", "setor", "cargo"]:
        if campo in dados:
            setattr(colaborador, campo, dados[campo])

    db.session.commit()

    return jsonify(colaborador.to_dict())


@bp.route("/<int:matricula>", methods=["DELETE"])
def excluir(matricula):
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    colaborador = db.session.get(Colaborador, matricula)

    if colaborador is None:
        return jsonify({"error": "Colaborador não encontrado"}), 404

    db.session.delete(colaborador)
    db.session.commit()

    return "", 204
