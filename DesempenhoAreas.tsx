'use client'

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts'

interface AreaData {
  area: string
  total: number
  acertos: number
  taxa_acerto: number
  cor: string
  [key: string]: string | number // Especificando tipos mais específicos
}

interface DesempenhoAreasProps {
  data: AreaData[]
  title?: string
  type?: 'pie' | 'bar'
}

export default function DesempenhoAreas({ 
  data, 
  title = "Desempenho por Área", 
  type = 'bar' 
}: DesempenhoAreasProps) {
  
  const COLORS = ['#8B5CF6', '#F59E0B', '#10B981', '#EF4444', '#3B82F6']

  const CustomTooltip = ({ active, payload }: { active?: boolean; payload?: Array<{ payload: AreaData }> }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow">
          <p className="font-medium">{data.area}</p>
          <p className="text-gray-600">
            Acertos: {data.acertos}/{data.total}
          </p>
          <p className="text-indigo-600">
            Taxa: {data.taxa_acerto}%
          </p>
        </div>
      )
    }
    return null
  }

  const CustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: {
    cx: number;
    cy: number;
    midAngle: number;
    innerRadius: number;
    outerRadius: number;
    percent: number;
  }) => {
    const RADIAN = Math.PI / 180
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5
    const x = cx + radius * Math.cos(-midAngle * RADIAN)
    const y = cy + radius * Math.sin(-midAngle * RADIAN)

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        fontSize={12}
        fontWeight="bold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    )
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-medium text-gray-900 mb-4">{title}</h3>
      
      {type === 'pie' ? (
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={100}
                fill="#8884d8"
                dataKey="taxa_acerto"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                type="number" 
                domain={[0, 100]}
                tick={{ fontSize: 12, fill: '#6B7280' }}
              />
              <YAxis 
                type="category" 
                dataKey="area"
                tick={{ fontSize: 12, fill: '#6B7280' }}
                width={120}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar 
                dataKey="taxa_acerto" 
                fill="#6366F1"
                radius={[0, 4, 4, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Legenda e estatísticas */}
      <div className="mt-4 space-y-3">
        {data.map((area, index) => (
          <div key={area.area} className="flex items-center justify-between">
            <div className="flex items-center">
              <div 
                className="w-4 h-4 rounded mr-3"
                style={{ backgroundColor: COLORS[index % COLORS.length] }}
              ></div>
              <span className="text-sm font-medium text-gray-700">{area.area}</span>
            </div>
            <div className="text-sm text-gray-600">
              {area.acertos}/{area.total} ({area.taxa_acerto}%)
            </div>
          </div>
        ))}
      </div>

      {/* Resumo */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-lg font-bold text-gray-900">
              {data.reduce((sum, area) => sum + area.total, 0)}
            </div>
            <div className="text-xs text-gray-600">Total</div>
          </div>
          <div>
            <div className="text-lg font-bold text-green-600">
              {data.reduce((sum, area) => sum + area.acertos, 0)}
            </div>
            <div className="text-xs text-gray-600">Acertos</div>
          </div>
          <div>
            <div className="text-lg font-bold text-indigo-600">
              {data.length > 0 ? 
                Math.round(data.reduce((sum, area) => sum + area.taxa_acerto, 0) / data.length) : 0
              }%
            </div>
            <div className="text-xs text-gray-600">Média</div>
          </div>
        </div>
      </div>
    </div>
  )
}

