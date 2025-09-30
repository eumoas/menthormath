from flask import Blueprint, jsonify, request
from src.services.openai_service import OpenAIService
from src.models.questao import Questao, db
from src.models.sessao_estudo import SessaoEstudo
import json

ia_bp = Blueprint('ia', __name__)
openai_service = OpenAIService()

@ia_bp.route('/gerar-questao', methods=['POST'])
def gerar_questao():
    """Gera uma nova questão usando IA"""
    data = request.json
    
    area = data.get('area', 'matematica')
    competencia = data.get('competencia')
    dificuldade = data.get('dificuldade', 'medio')
    
    # Validar parâmetros
    if area not in ['matematica', 'ciencias_natureza']:
        return jsonify({'error': 'Área deve ser "matematica" ou "ciencias_natureza"'}), 400
    
    if dificuldade not in ['facil', 'medio', 'dificil']:
        return jsonify({'error': 'Dificuldade deve ser "facil", "medio" ou "dificil"'}), 400
    
    try:
        # Gerar questão usando OpenAI
        questao_data = openai_service.gerar_questao(area, competencia, dificuldade)
        
        # Salvar questão no banco de dados
        questao = Questao(
            enunciado=questao_data['enunciado'],
            alternativa_a=questao_data['alternativa_a'],
            alternativa_b=questao_data['alternativa_b'],
            alternativa_c=questao_data['alternativa_c'],
            alternativa_d=questao_data['alternativa_d'],
            alternativa_e=questao_data['alternativa_e'],
            resposta_correta=questao_data['resposta_correta'],
            explicacao=questao_data['explicacao'],
            area=questao_data['area'],
            competencia=questao_data['competencia'],
            habilidade=questao_data['habilidade'],
            dificuldade=questao_data['dificuldade'],
            tags=questao_data['tags']
        )
        
        db.session.add(questao)
        db.session.commit()
        
        return jsonify(questao.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@ia_bp.route('/feedback-educativo', methods=['POST'])
def gerar_feedback_educativo():
    """Gera feedback educativo para uma resposta"""
    data = request.json
    
    questao_id = data.get('questao_id')
    resposta_usuario = data.get('resposta_usuario')
    
    if not questao_id or not resposta_usuario:
        return jsonify({'error': 'questao_id e resposta_usuario são obrigatórios'}), 400
    
    # Buscar questão
    questao = Questao.query.get(questao_id)
    if not questao:
        return jsonify({'error': 'Questão não encontrada'}), 404
    
    # Verificar se acertou
    acertou = resposta_usuario.upper() == questao.resposta_correta.upper()
    
    try:
        # Gerar feedback usando OpenAI
        feedback = openai_service.gerar_feedback_educativo(
            questao.to_dict(), 
            resposta_usuario.upper(), 
            acertou
        )
        
        return jsonify({
            'feedback': feedback,
            'acertou': acertou,
            'resposta_correta': questao.resposta_correta
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar feedback: {str(e)}'}), 500

@ia_bp.route('/atualizar-feedback-sessao', methods=['PUT'])
def atualizar_feedback_sessao():
    """Atualiza uma sessão de estudo com feedback da IA"""
    data = request.json
    
    sessao_id = data.get('sessao_id')
    
    if not sessao_id:
        return jsonify({'error': 'sessao_id é obrigatório'}), 400
    
    # Buscar sessão
    sessao = SessaoEstudo.query.get(sessao_id)
    if not sessao:
        return jsonify({'error': 'Sessão não encontrada'}), 404
    
    try:
        # Gerar feedback usando OpenAI
        feedback = openai_service.gerar_feedback_educativo(
            sessao.questao.to_dict(),
            sessao.resposta_usuario,
            sessao.acertou
        )
        
        # Atualizar sessão
        sessao.feedback_ia = feedback
        db.session.commit()
        
        return jsonify(sessao.to_dict())
        
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar feedback: {str(e)}'}), 500

@ia_bp.route('/gerar-questoes-lote', methods=['POST'])
def gerar_questoes_lote():
    """Gera múltiplas questões em lote"""
    data = request.json
    
    quantidade = data.get('quantidade', 5)
    area = data.get('area', 'matematica')
    dificuldade = data.get('dificuldade', 'medio')
    
    if quantidade > 10:
        return jsonify({'error': 'Máximo de 10 questões por lote'}), 400
    
    questoes_geradas = []
    erros = []
    
    for i in range(quantidade):
        try:
            questao_data = openai_service.gerar_questao(area, None, dificuldade)
            
            questao = Questao(
                enunciado=questao_data['enunciado'],
                alternativa_a=questao_data['alternativa_a'],
                alternativa_b=questao_data['alternativa_b'],
                alternativa_c=questao_data['alternativa_c'],
                alternativa_d=questao_data['alternativa_d'],
                alternativa_e=questao_data['alternativa_e'],
                resposta_correta=questao_data['resposta_correta'],
                explicacao=questao_data['explicacao'],
                area=questao_data['area'],
                competencia=questao_data['competencia'],
                habilidade=questao_data['habilidade'],
                dificuldade=questao_data['dificuldade'],
                tags=questao_data['tags']
            )
            
            db.session.add(questao)
            questoes_geradas.append(questao_data)
            
        except Exception as e:
            erros.append(f'Erro na questão {i+1}: {str(e)}')
    
    try:
        db.session.commit()
        return jsonify({
            'questoes_geradas': len(questoes_geradas),
            'questoes': questoes_geradas,
            'erros': erros
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao salvar questões: {str(e)}'}), 500

