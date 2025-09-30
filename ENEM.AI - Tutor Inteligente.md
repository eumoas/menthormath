# ENEM.AI - Tutor Inteligente

## 🎯 Sobre o Projeto

O **ENEM.AI** é um tutor inteligente desenvolvido especificamente para auxiliar estudantes na preparação para o ENEM (Exame Nacional do Ensino Médio), com foco nas áreas de **Matemática** e **Ciências da Natureza**.

Esta é uma versão **MVP (Mínimo Produto Viável)** que demonstra as funcionalidades principais da plataforma, incluindo geração de questões, feedback educativo e acompanhamento de progresso.

## 🚀 Aplicação Deployada

**URL de Acesso:** https://mzhyi8c1xwnd.manus.space

## 📋 Funcionalidades Implementadas

### ✅ Backend (Flask)
- **API RESTful** completa para gerenciamento de questões, usuários e sessões de estudo
- **Banco de dados SQLite** com modelos para usuários, questões e sessões
- **Sistema de estatísticas** com cálculo de taxa de acerto por área
- **Integração com OpenAI** (preparada, mas comentada no deploy)
- **CORS habilitado** para comunicação com frontend

### ✅ Frontend (Next.js + React)
- **Dashboard interativo** com visualizações de progresso
- **Sistema de questões** com interface intuitiva
- **Componentes de visualização** usando Recharts:
  - Radar de competências
  - Gráfico de progresso semanal
  - Análise de desempenho por área
- **Design responsivo** com TailwindCSS

### ✅ Funcionalidades Principais
- **Questões categorizadas** por área (Matemática/Ciências da Natureza)
- **Sistema de dificuldade** (Fácil, Médio, Difícil)
- **Feedback educativo** com explicações detalhadas
- **Acompanhamento de progresso** com estatísticas em tempo real
- **Interface moderna** e intuitiva

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para banco de dados
- **Flask-CORS** - Habilitação de CORS
- **SQLite** - Banco de dados
- **OpenAI API** - Integração para IA (preparada)

### Frontend
- **Next.js 15** - Framework React
- **React** - Biblioteca de interface
- **TypeScript** - Tipagem estática
- **TailwindCSS** - Framework CSS
- **Recharts** - Biblioteca de gráficos

## 📊 API Endpoints

### Questões
- `GET /api/questoes` - Listar todas as questões
- `GET /api/questoes/aleatoria` - Obter questão aleatória
- `GET /api/questoes/aleatoria?area=matematica` - Questão por área
- `GET /api/questoes/aleatoria?dificuldade=facil` - Questão por dificuldade

### Usuários
- `GET /api/users` - Listar usuários
- `GET /api/users/{id}` - Obter usuário específico

### Sessões de Estudo
- `POST /api/sessoes` - Criar nova sessão de estudo
- `GET /api/sessoes` - Listar sessões

### Estatísticas
- `GET /api/estatisticas/{user_id}` - Obter estatísticas do usuário

### IA (Preparado para futuras implementações)
- `POST /api/ia/gerar-questao` - Gerar questão com IA
- `POST /api/ia/feedback-educativo` - Obter feedback educativo

## 🗂️ Estrutura do Projeto

```
enem_ai/
├── backend/
│   └── enem_ai_backend/
│       ├── src/
│       │   ├── models/          # Modelos do banco de dados
│       │   ├── routes/          # Rotas da API
│       │   ├── services/        # Serviços (OpenAI, etc.)
│       │   ├── static/          # Arquivos estáticos
│       │   └── main.py          # Aplicação principal
│       └── requirements.txt     # Dependências Python
└── frontend/
    ├── src/
    │   ├── app/                 # Páginas Next.js
    │   └── components/          # Componentes React
    ├── package.json             # Dependências Node.js
    └── tailwind.config.js       # Configuração TailwindCSS
```

## 🎮 Como Usar

### 1. Acesse a Aplicação
Visite: https://mzhyi8c1xwnd.manus.space

### 2. Explore o Dashboard
- Visualize suas estatísticas de estudo
- Acompanhe seu progresso por área
- Analise seu desempenho nas competências

### 3. Pratique com Questões
- Use os filtros para selecionar área e dificuldade
- Responda às questões e receba feedback imediato
- Acompanhe sua evolução em tempo real

## 📈 Dados de Exemplo

O sistema vem pré-populado com:
- **6 questões de exemplo** (3 Matemática + 3 Ciências da Natureza)
- **3 usuários de teste**
- **Diferentes níveis de dificuldade**
- **Competências e habilidades do ENEM**

## 🔮 Próximos Passos

### Funcionalidades Planejadas
1. **Integração completa com OpenAI** para geração dinâmica de questões
2. **Sistema de autenticação** com login/registro
3. **Planos de estudo personalizados**
4. **Simulados completos do ENEM**
5. **Análise preditiva de desempenho**
6. **Gamificação** com pontuações e conquistas
7. **Relatórios detalhados** em PDF

### Melhorias Técnicas
1. **Deploy em produção** com PostgreSQL
2. **Cache Redis** para melhor performance
3. **Testes automatizados** completos
4. **Monitoramento** e logs
5. **PWA** para uso offline

## 👥 Desenvolvimento

Este projeto foi desenvolvido como um **MVP funcional** seguindo as especificações do PRD (Documento de Requisitos de Produto) fornecido, demonstrando todas as funcionalidades principais de um tutor inteligente para o ENEM.

### Arquitetura
- **Backend**: API RESTful em Flask
- **Frontend**: SPA em Next.js/React
- **Banco de Dados**: SQLite (MVP) → PostgreSQL (produção)
- **Deploy**: Manus Platform

## 📝 Licença

Este projeto foi desenvolvido como demonstração técnica e está disponível para fins educacionais.

---

**ENEM.AI** - Transformando a preparação para o ENEM com inteligência artificial! 🚀

