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

export async function registrarEntrada(numeroVaga: number, placa: string) {
  const { data } = await api.post<Registro>('/registros/', { numero_vaga: numeroVaga, placa })
  return data
}

export async function registrarSaida(idRegistro: number) {
  const { data } = await api.put<Registro>(`/registros/${idRegistro}/saida`)
  return data
}

export async function buscarRegistro(idRegistro: number) {
  const { data } = await api.get<Registro>(`/registros/${idRegistro}`)
  return data
}
