export type EstadoVaga = 'livre' | 'colaborador' | 'terceiro'

export type FiltroVagas = 'todas' | 'livre' | 'ocupada'

export interface VagaMapa {
  numero: number
  estado: EstadoVaga
}

export interface OcupacaoVaga {
  placa: string
  veiculo: string
  vinculo: string
  responsavel: string
  entrada: string
  guarda: string
}

export interface Movimentacao {
  placa: string
  descricao: string
  hora: string
}
