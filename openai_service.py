import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        )
    
    def gerar_questao(self, area: str, competencia: str = None, dificuldade: str = "medio") -> dict:
        """
        Gera uma questão usando a API OpenAI
        
        Args:
            area: "matematica" ou "ciencias_natureza"
            competencia: Competência específica (opcional)
            dificuldade: "facil", "medio" ou "dificil"
        
        Returns:
            dict: Questão gerada no formato esperado
        """
        
        area_nome = "Matemática" if area == "matematica" else "Ciências da Natureza"
        
        prompt = f"""
        Gere uma questão de {area_nome} para o ENEM com as seguintes características:
        - Área: {area_nome}
        - Dificuldade: {dificuldade}
        {f"- Competência: {competencia}" if competencia else ""}
        
        A questão deve seguir EXATAMENTE este formato JSON:
        {{
            "enunciado": "Texto do enunciado da questão",
            "alternativa_a": "Texto da alternativa A",
            "alternativa_b": "Texto da alternativa B", 
            "alternativa_c": "Texto da alternativa C",
            "alternativa_d": "Texto da alternativa D",
            "alternativa_e": "Texto da alternativa E",
            "resposta_correta": "A",
            "explicacao": "Explicação detalhada da resposta correta",
            "area": "{area}",
            "competencia": "Competência X",
            "habilidade": "HXX",
            "dificuldade": "{dificuldade}",
            "tags": ["tag1", "tag2", "tag3"]
        }}
        
        Requisitos:
        1. O enunciado deve ser claro e contextualizado
        2. As alternativas devem ser plausíveis
        3. A explicação deve ser didática e completa
        4. Use competências e habilidades reais do ENEM
        5. As tags devem ser relevantes ao conteúdo
        6. Responda APENAS com o JSON válido, sem texto adicional
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um especialista em criar questões do ENEM. Responda sempre com JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Tentar extrair JSON do conteúdo
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            questao_data = json.loads(content)
            
            # Validar campos obrigatórios
            required_fields = [
                'enunciado', 'alternativa_a', 'alternativa_b', 'alternativa_c',
                'alternativa_d', 'alternativa_e', 'resposta_correta', 'explicacao',
                'area', 'competencia', 'habilidade', 'dificuldade', 'tags'
            ]
            
            for field in required_fields:
                if field not in questao_data:
                    raise ValueError(f"Campo obrigatório '{field}' não encontrado")
            
            # Converter tags para JSON string se necessário
            if isinstance(questao_data['tags'], list):
                questao_data['tags'] = json.dumps(questao_data['tags'])
            
            return questao_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao decodificar JSON da resposta OpenAI: {e}")
        except Exception as e:
            raise ValueError(f"Erro ao gerar questão: {e}")
    
    def gerar_feedback_educativo(self, questao: dict, resposta_usuario: str, acertou: bool) -> str:
        """
        Gera feedback educativo personalizado para a resposta do usuário
        
        Args:
            questao: Dados da questão
            resposta_usuario: Resposta escolhida pelo usuário (A, B, C, D, E)
            acertou: Se o usuário acertou a questão
        
        Returns:
            str: Feedback educativo personalizado
        """
        
        status = "acertou" if acertou else "errou"
        alternativa_usuario = questao.get(f'alternativa_{resposta_usuario.lower()}', '')
        
        prompt = f"""
        Um estudante {status} uma questão de {questao['area']} do ENEM.
        
        Questão: {questao['enunciado']}
        
        Resposta correta: {questao['resposta_correta']} - {questao.get(f'alternativa_{questao["resposta_correta"].lower()}', '')}
        Resposta do estudante: {resposta_usuario} - {alternativa_usuario}
        
        Explicação oficial: {questao['explicacao']}
        
        Gere um feedback educativo personalizado que:
        1. {"Parabenize o acerto e reforce o aprendizado" if acertou else "Seja encorajador sobre o erro"}
        2. Explique o conceito de forma didática
        3. {"Dê dicas para questões similares" if acertou else "Identifique onde pode ter havido confusão"}
        4. Sugira próximos passos de estudo
        5. Mantenha um tom motivador e educativo
        
        Limite: 200 palavras
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um tutor educativo especializado em ENEM. Seja sempre encorajador e didático."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback para feedback padrão em caso de erro
            if acertou:
                return f"Parabéns! Você acertou a questão. {questao['explicacao']} Continue praticando para manter o bom desempenho!"
            else:
                return f"Não desanime! O erro faz parte do aprendizado. {questao['explicacao']} Revise o conteúdo e tente questões similares."

