import api from './api'

export interface Colaborador {
  matricula: number
  nome: string
  setor: string
  cargo: string
}

export async function listarColaboradores() {
  const { data } = await api.get<Colaborador[]>('/colaboradores/')
  return data
}

export async function buscarColaborador(matricula: number) {
  const { data } = await api.get<Colaborador>(`/colaboradores/${matricula}`)
  return data
}
