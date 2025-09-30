from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Questao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enunciado = db.Column(db.Text, nullable=False)
    alternativa_a = db.Column(db.Text, nullable=False)
    alternativa_b = db.Column(db.Text, nullable=False)
    alternativa_c = db.Column(db.Text, nullable=False)
    alternativa_d = db.Column(db.Text, nullable=False)
    alternativa_e = db.Column(db.Text, nullable=False)
    resposta_correta = db.Column(db.String(1), nullable=False)  # A, B, C, D ou E
    explicacao = db.Column(db.Text, nullable=False)
    area = db.Column(db.String(50), nullable=False)  # "matematica" ou "ciencias_natureza"
    competencia = db.Column(db.String(100), nullable=False)
    habilidade = db.Column(db.String(100), nullable=False)
    dificuldade = db.Column(db.String(20), nullable=False)  # "facil", "medio", "dificil"
    tags = db.Column(db.Text)  # JSON string com tags
    imagem_url = db.Column(db.String(255))  # URL da imagem se houver
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Questao {self.id} - {self.area}>'

    def to_dict(self):
        return {
            'id': self.id,
            'enunciado': self.enunciado,
            'alternativa_a': self.alternativa_a,
            'alternativa_b': self.alternativa_b,
            'alternativa_c': self.alternativa_c,
            'alternativa_d': self.alternativa_d,
            'alternativa_e': self.alternativa_e,
            'resposta_correta': self.resposta_correta,
            'explicacao': self.explicacao,
            'area': self.area,
            'competencia': self.competencia,
            'habilidade': self.habilidade,
            'dificuldade': self.dificuldade,
            'tags': self.tags,
            'imagem_url': self.imagem_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

