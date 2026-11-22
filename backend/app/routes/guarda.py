from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from app import db
from app.models.guarda import Guarda
from app.routes.login import autenticacao_obrigatoria
from app.validacao import campos_faltando

bp = Blueprint("guarda", __name__, url_prefix="/guardas")

TURNOS = {
    "manhã" : "Manhã",
    "tarde" : "Tarde",
    "noite" : "Noite", 
}

def normalizar_cpf(cpf):
    return ''.join(filter(str.isdigit, str(cpf)))


@bp.route("/", methods=["GET"])
@autenticacao_obrigatoria
def listar():
    guardas = db.session.execute(db.select(Guarda)).scalars()

    return jsonify([guarda.to_dict() for guarda in guardas])


@bp.route("/<string:cpf_guarda>", methods=["GET"])
@autenticacao_obrigatoria
def buscar(cpf_guarda):

    cpf_guarda = normalizar_cpf(cpf_guarda)

    if len(cpf_guarda) != 11:
        return jsonify({"error": "CPF inválido"}), 400
    
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

    cpf = normalizar_cpf(dados["cpf_guarda"])
    nome = dados["nome_guarda"]
    turno = dados["turno"]
    senha = dados["senha"]

    if len(cpf) != 11:
        return jsonify({"error":"O CPF deve conter 11 dígitos"}), 400

    if not isinstance(nome, str) or not nome.strip():
        return jsonify({"error": "Informe um nome válido"}), 400

    if not isinstance(turno, str) or turno.strip().casefold() not in TURNOS:
        return jsonify({"error":"Turno inválido"}), 400

    if not isinstance(senha, str) or len(senha) < 8:
        return jsonify({"error":"A senha deve ter pelo menos 8 caracteres"}), 400

    if db.session.get(Guarda, cpf) is not None:
        return jsonify({"error": "Guarda já cadastrado"}), 409

    guarda = Guarda(
        cpf_guarda=cpf,
        nome_guarda=nome.strip(),
        turno=TURNOS[turno.strip().casefold()],
        senha=generate_password_hash(senha),
    )
    db.session.add(guarda)
    db.session.commit()

    return jsonify(guarda.to_dict()), 201


@bp.route("/<string:cpf_guarda>", methods=["PUT"])
@autenticacao_obrigatoria
def editar(cpf_guarda):

    cpf_guarda = normalizar_cpf(cpf_guarda)

    if len(cpf_guarda) != 11:
        return jsonify({"error": "CPF inválido"}), 400

    guarda = db.session.get(Guarda, cpf_guarda)

    if guarda is None:
        return jsonify({"error": "Guarda não encontrado"}), 404

    dados = request.get_json(silent=True) or {}


    if not dados:
        return jsonify({"error": "Informe os dados para atualizar"}), 400

    if "nome_guarda" in dados:
        nome = dados["nome_guarda"]

        if not isinstance(nome, str) or not nome.strip():
            return jsonify({"error":"O nome não pode ficar vazio"}), 400

        guarda.nome_guarda = nome.strip()

    if "turno" in dados:
        turno = dados["turno"]

        if not isinstance(turno, str) or turno.strip().casefold() not in TURNOS:
            return jsonify({"error":"Turno inválido"}), 400

        guarda.turno = TURNOS[turno.strip().casefold()]

    db.session.commit()

    return jsonify(guarda.to_dict()), 200


@bp.route("/<string:cpf_guarda>", methods=["DELETE"])
@autenticacao_obrigatoria
def deletar(cpf_guarda):

    cpf_guarda = normalizar_cpf(cpf_guarda)

    if len(cpf_guarda) != 11:
        return jsonify({"error": "CPF inválido"}), 400

    guarda = db.session.get(Guarda, cpf_guarda)

    if guarda is None:
        return jsonify({"error": "Guarda não encontrado"}), 404

    db.session.delete(guarda)
    db.session.commit()

    return "", 204
