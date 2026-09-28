from datetime import datetime, timedelta
from decimal import Decimal

from flask import Blueprint, jsonify, request

from app import db
from app.models.pagamento import Pagamento
from app.models.registro import Registro
from app.routes.login import verificar_token

bp = Blueprint("pagamento", __name__, url_prefix="/pagamentos")


@bp.route("/", methods=["GET"])
def listar():
    guarda_logado = verificar_token()

    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    pagamentos = db.session.execute(db.select(Pagamento)).scalars().all()

    return jsonify([pagamento.to_dict() for pagamento in pagamentos])


@bp.route("/<int:id_pagamento>", methods=["GET"])
def buscar(id_pagamento):
    guarda_logado = verificar_token()

    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    pagamento = db.session.get(Pagamento, id_pagamento)

    if pagamento is None:
        return jsonify({"error": "Pagamento não encontrado"}), 404

    return jsonify(pagamento.to_dict())


@bp.route("/", methods=["POST"])
def criar():
    guarda_logado = verificar_token()

    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    dados = request.get_json(silent=True) or {}

    campos_obrigatorios = ["id_registro", "tipo_cartao"]
    faltando = [campo for campo in campos_obrigatorios if campo not in dados]
    if faltando:
        return jsonify(
            {"error": f"Campos obrigatórios não preenchidos: {', '.join(faltando)}"}
        ), 400

    registro = db.session.get(Registro, dados["id_registro"])

    if registro is None:
        return jsonify({"error": "Registro não encontrado"}), 404

    if registro.data_saida is None:
        return jsonify(
            {
                "error": "Não é possível criar um pagamento para um registro sem data de saída"
            }
        ), 400

    pagamento_existente = db.session.execute(
        db.select(Pagamento).where(Pagamento.id_registro == dados["id_registro"])
    ).scalar_one_or_none()

    if pagamento_existente is not None:
        return jsonify({"error": "Pagamento já existe para este registro"}), 409

    tempo = registro.data_saida - registro.data_entrada
    tempo_abonado = timedelta(minutes=30)

    if tempo <= tempo_abonado:
        valor = Decimal("0.00")
    else:
        tempo_cobrado = tempo - tempo_abonado
        minutos_cobrados = Decimal(str(tempo_cobrado.total_seconds() / 60))
        valor = (Decimal("3.00") / Decimal(60)) * minutos_cobrados

    agora = datetime.now()

    pagamento = Pagamento(
        id_registro=dados["id_registro"],
        valor=valor,
        data_pagamento=agora.date(),
        hora_pagamento=agora.time(),
        tipo_cartao=dados["tipo_cartao"],
        status_pagamento=True,
    )
    db.session.add(pagamento)
    db.session.commit()

    return jsonify(pagamento.to_dict()), 201
