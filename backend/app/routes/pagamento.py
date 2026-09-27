from flask import Blueprint, jsonify

from app import db
from app.models.pagamento import Pagamento
from app.routes.login import verificar_token


bp = Blueprint("pagamento", __name__, url_prefix="/pagamentos")


@bp.route("/", methods=["GET"])
def listar():
    guarda_logado = verificar_token()

    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    pagamentos = db.session.execute(
        db.select(Pagamento)
    ).scalars().all()

    return jsonify([
        pagamento.to_dict()
        for pagamento in pagamentos
    ])


@bp.route("/<int:id_pagamento>", methods=["GET"])
def buscar(id_pagamento):
    guarda_logado = verificar_token()

    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    pagamento = db.session.get(
        Pagamento,
        id_pagamento
    )

    if pagamento is None:
        return jsonify({
            "error": "Pagamento não encontrado"
        }), 404

    return jsonify(pagamento.to_dict())