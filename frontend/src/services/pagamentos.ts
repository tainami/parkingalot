import api from './api'

export interface Pagamento {
  id_pagamento: number
  id_registro: number
  valor: number
  data_pagamento: string
  hora_pagamento: string
  tipo_cartao: string | null
  status_pagamento: boolean
}

export async function listarPagamentos() {
  const { data } = await api.get<Pagamento[]>('/pagamentos/')
  return data
}
