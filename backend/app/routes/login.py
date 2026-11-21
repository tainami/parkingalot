import secrets
from functools import wraps

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

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


@bp.route("/logout", methods=["POST"])
def logout():
    guarda_logado = verificar_token()

    if guarda_logado is None:
        return jsonify({"error": "Não autorizado"}), 401

    guarda_logado.token = None
    db.session.commit()

    return jsonify({"message": "Logout realizado com sucesso"}), 200


def verificar_token():
    token = request.headers.get("Authorization")

    if not token:
        return None

    token = token.removeprefix("Bearer ")

    guarda = db.session.execute(
        db.select(Guarda).where(Guarda.token == token)
    ).scalar_one_or_none()

    return guarda


@bp.route('/redefinir-senha', methods=['POST'])
def redefinir_senha():
    dados = request.get_json()

    cpf = ''.join(filter(str.isdigit, str(dados.get('cpf_guarda'))))
    nome = dados.get('nome_guarda', '').strip()
    nova_senha = dados.get('nova_senha', '')
    confirmar_senha = dados.get('confirmar_senha', '')

    if not cpf or not nome or not nova_senha or not confirmar_senha:
        return jsonify({'error': 'Preencha todos os campos'}), 400

    if nova_senha != confirmar_senha:
        return jsonify({'error': 'As senhas não coincidem'}), 400

    if len(nova_senha) < 8:
        return jsonify({'error': 'A senha deve ter pelo menos 8 caracteres'}), 400

    guarda = Guarda.query.filter_by(cpf_guarda=cpf).first()

    if not guarda or guarda.nome_guarda.strip().casefold() != nome.casefold():
        return jsonify({'error': 'CPF ou nome não conferem'}), 400

    guarda.senha = generate_password_hash(nova_senha)

    guarda.token = None

    db.session.commit()

    return jsonify({
        'message': 'Senha redefinida com sucesso'
    }), 200

def autenticacao_obrigatoria(rota):
    @wraps(rota)
    def decorated(*args, **kwargs):
        if verificar_token() is None:
            return jsonify({"error": "Não autorizado"}), 401
        return rota(*args, **kwargs)

    return decorated
