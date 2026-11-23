import api from './api'

export interface Veiculo {
  placa: string
  modelo: string
  cor: string
  tipo_veiculo: 'CARRO' | 'MOTO'
  tipo_vinculo: 'COLABORADOR' | 'TERCEIRO'
  matricula_colaborador: number | null
  documento_responsavel: string | null
}

export async function listarVeiculos() {
  const { data } = await api.get<Veiculo[]>('/veiculos/')
  return data
}

export async function buscarVeiculo(placa: string) {
  const { data } = await api.get<Veiculo>(`/veiculos/${placa}`)
  return data
}

export type NovoVeiculo = Omit<Veiculo, 'matricula_colaborador' | 'documento_responsavel'> & {
  matricula_colaborador?: number | null
  documento_responsavel?: string | null
}

export async function criarVeiculo(veiculo: NovoVeiculo) {
  const { data } = await api.post<Veiculo>('/veiculos/', veiculo)
  return data
}
