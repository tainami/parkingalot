from flask import Blueprint, jsonify, request

from app import db
from app.models.vaga import Vaga
from app.routes.login import verificar_token

bp = Blueprint("vaga", __name__, url_prefix="/vagas")


@bp.route("/", methods=["GET"])
def listar_vagas():
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    vagas = db.session.execute(db.select(Vaga)).scalars()
    return jsonify([vaga.to_dict() for vaga in vagas])


@bp.route("/<int:numero>", methods=["GET"])
def buscar_vaga(numero):
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    vaga = db.session.get(Vaga, numero)
    if vaga is None:
        return jsonify({"error": "Vaga não encontrada"}), 404
    return jsonify(vaga.to_dict())


@bp.route("/", methods=["POST"])
def criar_vaga():
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    dados = request.get_json(silent=True) or {}
    campos_obrigatorios = ["numero", "tipo_vaga"]

    faltando = [campo for campo in campos_obrigatorios if campo not in dados]
    if faltando:
        return jsonify(
            {"error": f"Campos obrigatórios não preenchidos: {', '.join(faltando)}"}
        ), 400

    if dados["tipo_vaga"] not in ["COLABORADOR", "TERCEIRO"]:
        return jsonify({"error": "Tipo de vaga inválido"}), 400

    if db.session.get(Vaga, dados["numero"]) is not None:
        return jsonify({"error": "Vaga já existe"}), 409

    vaga = Vaga(numero=dados["numero"], tipo_vaga=dados["tipo_vaga"])

    db.session.add(vaga)
    db.session.commit()

    return jsonify(vaga.to_dict()), 201


@bp.route("/<int:numero>", methods=["PUT"])
def atualizar_vaga(numero):
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    vaga = db.session.get(Vaga, numero)

    if vaga is None:
        return jsonify({"error": "Vaga não encontrada"}), 404

    dados = request.get_json(silent=True) or {}

    if "tipo_vaga" in dados:
        if dados["tipo_vaga"] not in ["COLABORADOR", "TERCEIRO"]:
            return jsonify({"error": "Tipo de vaga inválido"}), 400
        vaga.tipo_vaga = dados["tipo_vaga"]

    db.session.commit()

    return jsonify(vaga.to_dict())
