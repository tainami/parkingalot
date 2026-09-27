from app.routes.colaborador import bp as colaborador_bp
from app.routes.guarda import bp as guarda_bp
from app.routes.login import bp as login_bp
from app.routes.vaga import bp as vaga_bp
from app.routes.veiculo import bp as veiculo_bp
from app.routes.registro import bp as registro_bp
from app.routes.pagamento import bp as pagamento_bp

blueprints = [
    colaborador_bp,
    guarda_bp,
    vaga_bp,
    login_bp,
    veiculo_bp,
    registro_bp,
    pagamento_bp,
]
