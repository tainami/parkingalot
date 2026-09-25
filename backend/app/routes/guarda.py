from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from app import db
from app.models.guarda import Guarda
from backend.app.routes.login import verificar_token

bp = Blueprint("guarda", __name__, url_prefix="/guardas")

@bp.route("/", methods=["GET"])
def listar():

    guarda_logado=verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401
    
    guardas = db.session.execute(db.select(Guarda)).scalars()

    return jsonify([guarda.to_dict() for guarda in guardas])

@bp.route("/<string:cpf_guarda>", methods=["GET"])
def buscar(cpf_guarda):
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401
    guarda = db.session.get(Guarda, cpf_guarda)

    if guarda is None:
        return jsonify({"error": "Guarda não encontrado"}), 404

    return jsonify(guarda.to_dict())

@bp.route("/", methods=["POST"])
def cadastrar():
    dados = request.get_json(silent=True) or {}
    campos_obrigatorios = ["cpf_guarda", "nome_guarda", "turno", "senha"]
    faltando = [campo for campo in campos_obrigatorios if not dados.get(campo)]
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
def editar(cpf_guarda):
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401
    
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
def deletar(cpf_guarda):
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401
    guarda = db.session.get(Guarda, cpf_guarda)

    if guarda is None:
        return jsonify({"error": "Guarda não encontrado"}), 404

    db.session.delete(guarda)
    db.session.commit()

    return jsonify({"message": "Guarda deletado com sucesso"}), 200
