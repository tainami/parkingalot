from flask import Blueprint, jsonify, request

from app import db
from app.models.veiculo import Veiculo
from app.models.vaga import Vaga
from app.models.registro import Registro
from app.routes.login import verificar_token
from datetime import datetime

from parkingalot.backend.app.models import registro

bp = Blueprint("registro", __name__, url_prefix="/registros")

@bp.route("/", methods=["GET"])
def listar():
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    registros = db.session.execute(db.select(Registro)).scalars()
    return jsonify([registro.to_dict() for registro in registros])

@bp.route("/<int:id_registro>", methods=["GET"])
def buscar(id_registro):
    guarda_logado = verificar_token()

    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    registro = db.session.get(Registro, id_registro)

    if registro is None:
        return jsonify({"error": "Registro não encontrado"}), 404

    return jsonify(registro.to_dict())


@bp.route("/", methods=["POST"])
def criar():
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    dados = request.get_json(silent=True) or {}
    campos_obrigatorios = ["numero_vaga", "placa"]
    faltando = [campo for campo in campos_obrigatorios if campo not in dados]
    if faltando:
        return jsonify(
            {"error": f"Campos obrigatórios não preenchidos: {', '.join(faltando)}"}
        ), 400

    veiculo = db.session.get(Veiculo, dados["placa"])
    if veiculo is None:
        return jsonify({"error": "Veículo não encontrado"}), 404

    vaga = db.session.get(Vaga, dados["numero_vaga"])
    if vaga is None:
        return jsonify({"error": "Vaga não encontrada"}), 404

    if vaga.status_vaga:
        return jsonify({"error": "Vaga já ocupada"}), 409

    vaga.status_vaga = True
    data_entrada = datetime.now()

    registro = Registro(
        numero_vaga=dados["numero_vaga"],
        placa=dados["placa"],
        cpf_guarda=guarda_logado.cpf_guarda,
        data_entrada=data_entrada,
    )
    db.session.add(registro)
    db.session.commit()

    return jsonify(registro.to_dict()), 201

@bp.route("/<int:id_registro>/saida", methods=["PUT"])
def saida(id_registro):
    guarda_logado = verificar_token()
    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401
    
    registro = db.session.get(Registro, id_registro)
    if registro is None:
        return jsonify({"error": "Registro não encontrado"}), 404

    if registro.data_saida is not None:
        return jsonify({"error": "Registro já possui data de saída"}), 400

    registro.data_saida = datetime.now()

    vaga = db.session.get(Vaga, registro.numero_vaga)
    if vaga is None:
        return jsonify({"error": "Vaga não encontrada"}), 404

    vaga.status_vaga = False
    db.session.commit()
    return jsonify(registro.to_dict()), 200

@bp.route("/<int:id_registro>", methods=["PUT"])
def atualizar(id_registro):
    guarda_logado = verificar_token()

    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    registro = db.session.get(Registro, id_registro)

    if registro is None:
        return jsonify({"error": "Registro não encontrado"}), 404

    dados = request.get_json(silent=True) or {}
    
