from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class SessaoEstudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), nullable=False)
    resposta_usuario = db.Column(db.String(1), nullable=False)  # A, B, C, D ou E
    acertou = db.Column(db.Boolean, nullable=False)
    tempo_resposta = db.Column(db.Integer)  # tempo em segundos
    feedback_ia = db.Column(db.Text)  # feedback gerado pela IA
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    user = db.relationship('User', backref=db.backref('sessoes_estudo', lazy=True))
    questao = db.relationship('Questao', backref=db.backref('sessoes_estudo', lazy=True))

    def __repr__(self):
        return f'<SessaoEstudo {self.id} - User {self.user_id} - Questao {self.questao_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'questao_id': self.questao_id,
            'resposta_usuario': self.resposta_usuario,
            'acertou': self.acertou,
            'tempo_resposta': self.tempo_resposta,
            'feedback_ia': self.feedback_ia,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

