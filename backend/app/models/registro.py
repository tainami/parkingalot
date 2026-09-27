from app import db


class Registro(db.Model):
    __tablename__ = "registro"

    id_registro = db.Column(db.Integer, primary_key=True)
    numero_vaga = db.Column(db.Integer, db.ForeignKey("vaga.numero"), nullable=False)
    placa = db.Column(db.String(7), db.ForeignKey("veiculo.placa"), nullable=False)
    cpf_guarda = db.Column(db.String(11), db.ForeignKey("guarda.cpf_guarda"), nullable=False)
    data_entrada = db.Column(db.DateTime, nullable=False)
    data_saida = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id_registro": self.id_registro,
            "numero_vaga": self.numero_vaga,
            "placa": self.placa,
            "cpf_guarda": self.cpf_guarda,
            "data_entrada": self.data_entrada,
            "data_saida": self.data_saida,
        }

