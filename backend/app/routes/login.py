import secrets

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from app import db
from app.models.guarda import Guarda

bp = Blueprint("login", __name__, url_prefix="/login")


@bp.route("/", methods=["POST"])
def login():
    dados = request.get_json(silent=True) or {}

    cpf = dados.get("cpf_guarda")
    senha = dados.get("senha")

    if not cpf or not senha:
        return jsonify({"error": "CPF e senha são obrigatórios"}), 400

    guarda = db.session.get(Guarda, cpf)

    if guarda is None or not check_password_hash(guarda.senha, senha):
        return jsonify({"error": "CPF ou senha inválidos"}), 401

    token = secrets.token_hex(32)
    guarda.token = token
    db.session.commit()

    return jsonify(
        {
            "message": "Login realizado com sucesso",
            "token": token,
            "guarda": guarda.to_dict(),
        }
    ), 200


def verificar_token():
    token = request.headers.get("Authorization")

    if not token:
        return None

    token = token.removeprefix("Bearer ")

    guarda = db.session.execute(
        db.select(Guarda).where(Guarda.token == token)
    ).scalar_one_or_none()

    return guarda
