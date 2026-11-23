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

export async function criarVaga(numero: number) {
  const { data } = await api.post<Vaga>('/vagas/', { numero })
  return data
}

export async function atualizarVaga(numeroAtual: number, novoNumero: number) {
  const { data } = await api.put<Vaga>(`/vagas/${numeroAtual}`, { numero: novoNumero })
  return data
}
