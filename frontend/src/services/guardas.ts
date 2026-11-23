import api from './api'

export interface Guarda {
  cpf_guarda: string
  nome_guarda: string
  turno: string
}

export async function listarGuardas() {
  const { data } = await api.get<Guarda[]>('/guardas/')
  return data
}

export async function buscarGuarda(cpf: string) {
  const { data } = await api.get<Guarda>(`/guardas/${cpf}`)
  return data
}
