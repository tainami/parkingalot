import api from './api'

export interface Registro {
  id_registro: number
  numero_vaga: number
  placa: string
  cpf_guarda: string
  data_entrada: string
  data_saida: string | null
}

export async function listarRegistros(filtros: { data?: string } = {}) {
  const { data } = await api.get<Registro[]>('/registros/', { params: filtros })
  return data
}
