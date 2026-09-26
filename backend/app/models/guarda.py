from app import db


class Guarda(db.Model):
    __tablename__ = "guarda"

    cpf_guarda = db.Column(db.String(11), primary_key=True)
    nome_guarda = db.Column(db.String(100), nullable=False)
    turno = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "cpf_guarda": self.cpf_guarda,
            "nome_guarda": self.nome_guarda,
            "turno": self.turno,
        }
