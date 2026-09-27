from app import db


class Pagamento(db.Model):
    __tablename__ = "pagamento"

    id_pagamento = db.Column(db.Integer, primary_key=True)
    id_registro = db.Column(
        db.Integer,
        db.ForeignKey("registro.id_registro"),
        nullable=False
    )
    valor = db.Column(db.Numeric, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False)
    hora_pagamento = db.Column(db.Time, nullable=False)
    tipo_cartao = db.Column(db.String(50), nullable=True)
    status_pagamento = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "id_pagamento": self.id_pagamento,
            "id_registro": self.id_registro,
            "valor": self.valor,
            "data_pagamento": self.data_pagamento,
            "hora_pagamento": self.hora_pagamento,
            "tipo_cartao": self.tipo_cartao,
            "status_pagamento": self.status_pagamento,
        }