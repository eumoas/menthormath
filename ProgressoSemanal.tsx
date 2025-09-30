'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'

interface ProgressoData {
  semana: string
  questoes_resolvidas: number
  acertos?: number
  taxa_acerto?: number
}

interface ProgressoSemanalProps {
  data: ProgressoData[]
  title?: string
  type?: 'line' | 'bar'
}

export default function ProgressoSemanal({ 
  data, 
  title = "Progresso Semanal", 
  type = 'bar' 
}: ProgressoSemanalProps) {
  
  const CustomTooltip = ({ active, payload, label }: {
    active?: boolean;
    payload?: Array<{ value: number; payload: ProgressoData }>;
    label?: string;
  }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow">
          <p className="font-medium">{label}</p>
          <p className="text-indigo-600">
            Questões: {payload[0].value}
          </p>
          {payload[0].payload.taxa_acerto && (
            <p className="text-green-600">
              Taxa de acerto: {payload[0].payload.taxa_acerto}%
            </p>
          )}
        </div>
      )
    }
    return null
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-medium text-gray-900 mb-4">{title}</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          {type === 'line' ? (
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="semana" 
                tick={{ fontSize: 12, fill: '#6B7280' }}
              />
              <YAxis 
                tick={{ fontSize: 12, fill: '#6B7280' }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line
                type="monotone"
                dataKey="questoes_resolvidas"
                stroke="#6366F1"
                strokeWidth={3}
                dot={{ fill: '#6366F1', strokeWidth: 2, r: 6 }}
                activeDot={{ r: 8, stroke: '#6366F1', strokeWidth: 2 }}
              />
            </LineChart>
          ) : (
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="semana" 
                tick={{ fontSize: 12, fill: '#6B7280' }}
              />
              <YAxis 
                tick={{ fontSize: 12, fill: '#6B7280' }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar 
                dataKey="questoes_resolvidas" 
                fill="#6366F1"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
        <div className="text-center">
          <div className="text-2xl font-bold text-indigo-600">
            {data.reduce((sum, item) => sum + item.questoes_resolvidas, 0)}
          </div>
          <div className="text-gray-600">Total de Questões</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">
            {data.length > 0 ? Math.round(data.reduce((sum, item) => sum + item.questoes_resolvidas, 0) / data.length) : 0}
          </div>
          <div className="text-gray-600">Média Semanal</div>
        </div>
      </div>
    </div>
  )
}

