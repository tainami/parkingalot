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
