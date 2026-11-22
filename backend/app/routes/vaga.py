from flask import Blueprint, jsonify, request

from app import db
from app.models.vaga import Vaga
from app.routes.login import autenticacao_obrigatoria

bp = Blueprint("vaga", __name__, url_prefix="/vagas")


@bp.route("/", methods=["GET"])
@autenticacao_obrigatoria
def listar_vagas():
    vagas = db.session.execute(db.select(Vaga)).scalars()
    return jsonify([vaga.to_dict() for vaga in vagas])


@bp.route("/<int:numero>", methods=["GET"])
@autenticacao_obrigatoria
def buscar_vaga(numero):
    vaga = db.session.get(Vaga, numero)
    if vaga is None:
        return jsonify({"error": "Vaga não encontrada"}), 404
    return jsonify(vaga.to_dict())


@bp.route("/", methods=["POST"])
@autenticacao_obrigatoria
def criar_vaga():
    dados = request.get_json(silent=True) or {}

    if 'numero' not in dados:
        return jsonify({"error": "Informe o número da vaga"}), 400

    if db.session.get(Vaga, dados["numero"]) is not None:
        return jsonify({"error": "Vaga já existe"}), 409

    vaga = Vaga(
       numero=dados["numero"],
       tipo_vaga="COLABORADOR"
   )

    db.session.add(vaga)
    db.session.commit()

    return jsonify(vaga.to_dict()), 201
                      


@bp.route("/<int:numero>", methods=["PUT"])
@autenticacao_obrigatoria
def atualizar_vaga(numero):
    vaga = db.session.get(Vaga, numero)

    if vaga is None:
        return jsonify({"error": "Vaga não encontrada"}), 404

    dados = request.get_json(silent=True) or {}

    if "numero" not in dados:
        return jsonify({"error":"Informe o novo número da vaga"}), 400

    novo_numero = dados["numero"]

    if not isinstance(novo_numero, int) or isinstance(novo_numero, bool) or novo_numero <=0:
        return jsonify({"error":"Número da vaga inválido"}), 400

    if novo_numero != numero and db.session.get(Vaga, novo_numero) is not None:
        return jsonify({"error":"Já existe uma vaga com esse número"}), 409

    vaga.numero = novo_numero
    
    db.session.commit()

    return jsonify(vaga.to_dict())
