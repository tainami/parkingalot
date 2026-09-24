from app import db


class Colaborador(db.Model):
    __tablename__ = "colaborador"

    matricula = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    setor = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "matricula": self.matricula,
            "nome": self.nome,
            "setor": self.setor,
            "cargo": self.cargo,
        }
