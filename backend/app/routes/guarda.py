from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from app import db
from app.models.guarda import Guarda
from app.routes.login import autenticacao_obrigatoria
from app.validacao import campos_faltando

bp = Blueprint("guarda", __name__, url_prefix="/guardas")


@bp.route("/", methods=["GET"])
@autenticacao_obrigatoria
def listar():
    guardas = db.session.execute(db.select(Guarda)).scalars()

    return jsonify([guarda.to_dict() for guarda in guardas])


@bp.route("/<string:cpf_guarda>", methods=["GET"])
@autenticacao_obrigatoria
def buscar(cpf_guarda):
    guarda = db.session.get(Guarda, cpf_guarda)

    if guarda is None:
        return jsonify({"error": "Guarda não encontrado"}), 404

    return jsonify(guarda.to_dict())


@bp.route("/", methods=["POST"])
@autenticacao_obrigatoria
def cadastrar():
    dados = request.get_json(silent=True) or {}
    faltando = campos_faltando(dados, ["cpf_guarda", "nome_guarda", "turno", "senha"])
    if faltando:
        return jsonify(
            {"error": f"Campos obrigatórios faltando: {', '.join(faltando)}"}
        ), 400

    if db.session.get(Guarda, dados["cpf_guarda"]) is not None:
        return jsonify({"error": "Guarda já cadastrado"}), 409

    guarda = Guarda(
        cpf_guarda=dados["cpf_guarda"],
        nome_guarda=dados["nome_guarda"],
        turno=dados["turno"],
        senha=generate_password_hash(dados["senha"]),
    )
    db.session.add(guarda)
    db.session.commit()

    return jsonify(guarda.to_dict()), 201


@bp.route("/<string:cpf_guarda>", methods=["PUT"])
@autenticacao_obrigatoria
def editar(cpf_guarda):
    guarda = db.session.get(Guarda, cpf_guarda)

    if guarda is None:
        return jsonify({"error": "Guarda não encontrado"}), 404

    dados = request.get_json(silent=True) or {}

    if "senha" in dados:
        guarda.senha = generate_password_hash(dados["senha"])

    for campo in ["nome_guarda", "turno"]:
        if campo in dados:
            setattr(guarda, campo, dados[campo])

    db.session.commit()

    return jsonify(guarda.to_dict())


@bp.route("/<string:cpf_guarda>", methods=["DELETE"])
@autenticacao_obrigatoria
def deletar(cpf_guarda):
    guarda = db.session.get(Guarda, cpf_guarda)

    if guarda is None:
        return jsonify({"error": "Guarda não encontrado"}), 404

    db.session.delete(guarda)
    db.session.commit()

    return "", 204
