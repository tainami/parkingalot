import api from './api'

export interface Vaga {
  numero: number
  tipo_vaga: 'COLABORADOR' | 'TERCEIRO'
  status_vaga: boolean
}

export async function listarVagas() {
  const { data } = await api.get<Vaga[]>('/vagas/')
  return data
}
