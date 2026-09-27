from app import db


class Veiculo(db.Model):
    __tablename__ = "veiculo"

    placa = db.Column(db.String(7), primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    cor = db.Column(db.String(50), nullable=False)
    tipo_veiculo = db.Column(db.Enum("CARRO", "MOTO"), nullable=False)
    tipo_vinculo = db.Column(db.Enum("COLABORADOR", "TERCEIRO"), nullable=False)
    matricula_colaborador = db.Column(
        db.Integer, db.ForeignKey("colaborador.matricula"), nullable=True
    )
    documento_responsavel = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            "placa": self.placa,
            "modelo": self.modelo,
            "cor": self.cor,
            "tipo_veiculo": self.tipo_veiculo,
            "tipo_vinculo": self.tipo_vinculo,
            "matricula_colaborador": self.matricula_colaborador,
            "documento_responsavel": self.documento_responsavel,
        }
