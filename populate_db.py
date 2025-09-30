import os
import sys
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db, User
from src.models.questao import Questao
from src.models.sessao_estudo import SessaoEstudo
from src.main import app

def create_sample_questions():
    """Cria questões de exemplo para popular o banco de dados"""
    
    questoes_matematica = [
        {
            "enunciado": "Uma função f é definida por f(x) = 2x + 3. Qual é o valor de f(5)?",
            "alternativa_a": "10",
            "alternativa_b": "11", 
            "alternativa_c": "12",
            "alternativa_d": "13",
            "alternativa_e": "14",
            "resposta_correta": "D",
            "explicacao": "Para encontrar f(5), substituímos x por 5 na função: f(5) = 2(5) + 3 = 10 + 3 = 13",
            "area": "matematica",
            "competencia": "Competência 5",
            "habilidade": "H21",
            "dificuldade": "facil",
            "tags": json.dumps(["funcoes", "algebra", "substituicao"])
        },
        {
            "enunciado": "Em um triângulo retângulo, os catetos medem 3 cm e 4 cm. Qual é a medida da hipotenusa?",
            "alternativa_a": "5 cm",
            "alternativa_b": "6 cm",
            "alternativa_c": "7 cm", 
            "alternativa_d": "8 cm",
            "alternativa_e": "9 cm",
            "resposta_correta": "A",
            "explicacao": "Pelo teorema de Pitágoras: h² = 3² + 4² = 9 + 16 = 25, logo h = 5 cm",
            "area": "matematica",
            "competencia": "Competência 2",
            "habilidade": "H7",
            "dificuldade": "facil",
            "tags": json.dumps(["geometria", "pitagoras", "triangulo"])
        },
        {
            "enunciado": "Qual é a derivada da função f(x) = x³ + 2x² - 5x + 1?",
            "alternativa_a": "3x² + 4x - 5",
            "alternativa_b": "3x² + 2x - 5",
            "alternativa_c": "x² + 4x - 5",
            "alternativa_d": "3x² + 4x + 5",
            "alternativa_e": "3x + 4x - 5",
            "resposta_correta": "A",
            "explicacao": "Aplicando a regra da derivação: f'(x) = 3x² + 2(2x) - 5 = 3x² + 4x - 5",
            "area": "matematica",
            "competencia": "Competência 5",
            "habilidade": "H21",
            "dificuldade": "medio",
            "tags": json.dumps(["calculo", "derivadas", "polinomios"])
        }
    ]
    
    questoes_ciencias = [
        {
            "enunciado": "Qual é a fórmula química da água?",
            "alternativa_a": "H₂O",
            "alternativa_b": "CO₂",
            "alternativa_c": "NaCl",
            "alternativa_d": "CH₄",
            "alternativa_e": "O₂",
            "resposta_correta": "A",
            "explicacao": "A água é formada por dois átomos de hidrogênio (H) e um átomo de oxigênio (O), resultando na fórmula H₂O",
            "area": "ciencias_natureza",
            "competencia": "Competência 3",
            "habilidade": "H10",
            "dificuldade": "facil",
            "tags": json.dumps(["quimica", "moleculas", "agua"])
        },
        {
            "enunciado": "Qual é a velocidade da luz no vácuo?",
            "alternativa_a": "300.000 km/s",
            "alternativa_b": "299.792.458 m/s",
            "alternativa_c": "3 × 10⁸ m/s",
            "alternativa_d": "Todas as alternativas anteriores estão corretas",
            "alternativa_e": "Nenhuma das alternativas está correta",
            "resposta_correta": "D",
            "explicacao": "A velocidade da luz no vácuo é aproximadamente 300.000 km/s, que equivale a 299.792.458 m/s ou 3 × 10⁸ m/s",
            "area": "ciencias_natureza",
            "competencia": "Competência 2",
            "habilidade": "H6",
            "dificuldade": "medio",
            "tags": json.dumps(["fisica", "luz", "velocidade"])
        },
        {
            "enunciado": "Qual processo celular é responsável pela produção de ATP nas mitocôndrias?",
            "alternativa_a": "Fotossíntese",
            "alternativa_b": "Respiração celular",
            "alternativa_c": "Fermentação",
            "alternativa_d": "Digestão",
            "alternativa_e": "Excreção",
            "resposta_correta": "B",
            "explicacao": "A respiração celular é o processo que ocorre nas mitocôndrias para produzir ATP (energia) a partir da glicose e oxigênio",
            "area": "ciencias_natureza",
            "competencia": "Competência 1",
            "habilidade": "H4",
            "dificuldade": "medio",
            "tags": json.dumps(["biologia", "celula", "mitocondria", "ATP"])
        }
    ]
    
    return questoes_matematica + questoes_ciencias

def create_sample_users():
    """Cria usuários de exemplo"""
    users = [
        {"username": "estudante1", "email": "estudante1@email.com"},
        {"username": "estudante2", "email": "estudante2@email.com"},
        {"username": "admin", "email": "admin@email.com"}
    ]
    return users

def populate_database():
    """Popula o banco de dados com dados de exemplo"""
    with app.app_context():
        # Limpar dados existentes
        db.drop_all()
        db.create_all()
        
        print("Criando usuários de exemplo...")
        users_data = create_sample_users()
        for user_data in users_data:
            user = User(username=user_data["username"], email=user_data["email"])
            db.session.add(user)
        
        print("Criando questões de exemplo...")
        questoes_data = create_sample_questions()
        for questao_data in questoes_data:
            questao = Questao(**questao_data)
            db.session.add(questao)
        
        db.session.commit()
        print(f"Banco de dados populado com {len(users_data)} usuários e {len(questoes_data)} questões!")

if __name__ == "__main__":
    populate_database()

