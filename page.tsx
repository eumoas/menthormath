'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface Questao {
  id: number
  enunciado: string
  alternativa_a: string
  alternativa_b: string
  alternativa_c: string
  alternativa_d: string
  alternativa_e: string
  resposta_correta: string
  explicacao: string
  area: string
  competencia: string
  habilidade: string
  dificuldade: string
}

export default function EstudoPage() {
  const [questao, setQuestao] = useState<Questao | null>(null)
  const [respostaSelecionada, setRespostaSelecionada] = useState<string>('')
  const [mostrarResultado, setMostrarResultado] = useState(false)
  const [acertou, setAcertou] = useState(false)
  const [loading, setLoading] = useState(false)
  const [areaFiltro, setAreaFiltro] = useState<string>('')
  const [dificuldadeFiltro, setDificuldadeFiltro] = useState<string>('')
  const [userId] = useState(1) // Por simplicidade, usando usuário fixo

  useEffect(() => {
    buscarNovaQuestao()
  }, [])

  const buscarNovaQuestao = async () => {
    setLoading(true)
    setMostrarResultado(false)
    setRespostaSelecionada('')
    
    try {
      let url = 'http://localhost:5000/api/questoes/aleatoria'
      const params = new URLSearchParams()
      
      if (areaFiltro) params.append('area', areaFiltro)
      if (dificuldadeFiltro) params.append('dificuldade', dificuldadeFiltro)
      
      if (params.toString()) {
        url += '?' + params.toString()
      }
      
      const response = await fetch(url)
      if (response.ok) {
        const data = await response.json()
        setQuestao(data)
      } else {
        console.error('Erro ao buscar questão')
      }
    } catch (error) {
      console.error('Erro ao buscar questão:', error)
    } finally {
      setLoading(false)
    }
  }

  const submeterResposta = async () => {
    if (!respostaSelecionada || !questao) return

    const acertouQuestao = respostaSelecionada === questao.resposta_correta
    setAcertou(acertouQuestao)
    setMostrarResultado(true)

    // Salvar sessão de estudo
    try {
      await fetch('http://localhost:5000/api/sessoes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          questao_id: questao.id,
          resposta_usuario: respostaSelecionada,
          tempo_resposta: 60 // Por simplicidade, usando tempo fixo
        })
      })
    } catch (error) {
      console.error('Erro ao salvar sessão:', error)
    }
  }

  const alternativas = questao ? [
    { letra: 'A', texto: questao.alternativa_a },
    { letra: 'B', texto: questao.alternativa_b },
    { letra: 'C', texto: questao.alternativa_c },
    { letra: 'D', texto: questao.alternativa_d },
    { letra: 'E', texto: questao.alternativa_e }
  ] : []

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-gray-900">ENEM.AI</h1>
              <span className="ml-2 text-sm text-gray-500">Tutor Inteligente</span>
            </div>
            <nav className="flex space-x-8">
              <Link href="/" className="text-gray-500 hover:text-gray-700">
                Dashboard
              </Link>
              <Link href="/estudo" className="text-indigo-600 hover:text-indigo-500 font-medium">
                Estudar
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Filtros */}
          <div className="bg-white rounded-lg shadow mb-6 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Filtros</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Área
                </label>
                <select
                  value={areaFiltro}
                  onChange={(e) => setAreaFiltro(e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">Todas as áreas</option>
                  <option value="matematica">Matemática</option>
                  <option value="ciencias_natureza">Ciências da Natureza</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Dificuldade
                </label>
                <select
                  value={dificuldadeFiltro}
                  onChange={(e) => setDificuldadeFiltro(e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">Todas as dificuldades</option>
                  <option value="facil">Fácil</option>
                  <option value="medio">Médio</option>
                  <option value="dificil">Difícil</option>
                </select>
              </div>
              <div className="flex items-end">
                <button
                  onClick={buscarNovaQuestao}
                  disabled={loading}
                  className="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                  {loading ? 'Carregando...' : 'Nova Questão'}
                </button>
              </div>
            </div>
          </div>

          {/* Questão */}
          {questao && (
            <div className="bg-white rounded-lg shadow p-6">
              {/* Metadados da questão */}
              <div className="flex flex-wrap gap-2 mb-4">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {questao.area === 'matematica' ? 'Matemática' : 'Ciências da Natureza'}
                </span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                  {questao.competencia}
                </span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                  {questao.habilidade}
                </span>
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  questao.dificuldade === 'facil' ? 'bg-green-100 text-green-800' :
                  questao.dificuldade === 'medio' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {questao.dificuldade === 'facil' ? 'Fácil' : 
                   questao.dificuldade === 'medio' ? 'Médio' : 'Difícil'}
                </span>
              </div>

              {/* Enunciado */}
              <div className="mb-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">
                  Questão {questao.id}
                </h2>
                <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                  {questao.enunciado}
                </p>
              </div>

              {/* Alternativas */}
              <div className="space-y-3 mb-6">
                {alternativas.map((alternativa) => (
                  <label
                    key={alternativa.letra}
                    className={`flex items-start p-4 border rounded-lg cursor-pointer transition-colors ${
                      respostaSelecionada === alternativa.letra
                        ? 'border-indigo-500 bg-indigo-50'
                        : 'border-gray-200 hover:border-gray-300'
                    } ${
                      mostrarResultado
                        ? alternativa.letra === questao.resposta_correta
                          ? 'border-green-500 bg-green-50'
                          : alternativa.letra === respostaSelecionada && !acertou
                          ? 'border-red-500 bg-red-50'
                          : 'border-gray-200'
                        : ''
                    }`}
                  >
                    <input
                      type="radio"
                      name="resposta"
                      value={alternativa.letra}
                      checked={respostaSelecionada === alternativa.letra}
                      onChange={(e) => setRespostaSelecionada(e.target.value)}
                      disabled={mostrarResultado}
                      className="mt-1 mr-3"
                    />
                    <div>
                      <span className="font-medium text-gray-900">
                        {alternativa.letra})
                      </span>
                      <span className="ml-2 text-gray-700">
                        {alternativa.texto}
                      </span>
                    </div>
                  </label>
                ))}
              </div>

              {/* Botões de ação */}
              {!mostrarResultado ? (
                <button
                  onClick={submeterResposta}
                  disabled={!respostaSelecionada}
                  className="w-full bg-indigo-600 text-white px-4 py-3 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Confirmar Resposta
                </button>
              ) : (
                <div>
                  {/* Resultado */}
                  <div className={`p-4 rounded-lg mb-4 ${
                    acertou ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
                  }`}>
                    <div className="flex items-center">
                      <span className={`text-lg font-semibold ${
                        acertou ? 'text-green-800' : 'text-red-800'
                      }`}>
                        {acertou ? '✅ Correto!' : '❌ Incorreto'}
                      </span>
                    </div>
                    <p className={`mt-2 ${acertou ? 'text-green-700' : 'text-red-700'}`}>
                      A resposta correta é: <strong>{questao.resposta_correta}</strong>
                    </p>
                  </div>

                  {/* Explicação */}
                  <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg mb-4">
                    <h4 className="font-semibold text-blue-900 mb-2">Explicação:</h4>
                    <p className="text-blue-800 leading-relaxed">
                      {questao.explicacao}
                    </p>
                  </div>

                  <button
                    onClick={buscarNovaQuestao}
                    className="w-full bg-indigo-600 text-white px-4 py-3 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    Próxima Questão
                  </button>
                </div>
              )}
            </div>
          )}

          {loading && (
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <div className="text-xl text-gray-600">Carregando questão...</div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

