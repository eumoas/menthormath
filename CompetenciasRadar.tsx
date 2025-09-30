'use client'

import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts'

interface CompetenciaData {
  competencia: string
  valor: number
  fullMark: number
}

interface CompetenciasRadarProps {
  data: CompetenciaData[]
  title?: string
}

export default function CompetenciasRadar({ data, title = "Desempenho por Competência" }: CompetenciasRadarProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-medium text-gray-900 mb-4">{title}</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={data}>
            <PolarGrid />
            <PolarAngleAxis 
              dataKey="competencia" 
              tick={{ fontSize: 12, fill: '#6B7280' }}
            />
            <PolarRadiusAxis 
              angle={90} 
              domain={[0, 100]} 
              tick={{ fontSize: 10, fill: '#9CA3AF' }}
            />
            <Radar
              name="Desempenho"
              dataKey="valor"
              stroke="#6366F1"
              fill="#6366F1"
              fillOpacity={0.3}
              strokeWidth={2}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 text-sm text-gray-600">
        <p>Visualização do desempenho em cada competência do ENEM (0-100%)</p>
      </div>
    </div>
  )
}

