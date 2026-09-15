from flask import Blueprint, jsonify

bp = Blueprint("registro", __name__, url_prefix="/registros")

@bp.route("/", methods=["GET"])
def listar():
    return jsonify([])