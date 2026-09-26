from app import db


class Vaga(db.Model):
    __tablename__ = "vaga"

    numero = db.Column(db.Integer, primary_key=True)
    tipo_vaga = db.Column(db.Enum("COLABORADOR", "TERCEIRO"), nullable=False)
    status_vaga = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            "numero": self.numero,
            "tipo_vaga": self.tipo_vaga,
            "status_vaga": self.status_vaga,
        }
