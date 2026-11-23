function partes(valor: string) {
  const data = new Date(valor)
  return {
    dia: String(data.getUTCDate()).padStart(2, '0'),
    mes: String(data.getUTCMonth() + 1).padStart(2, '0'),
    hora: String(data.getUTCHours()).padStart(2, '0'),
    minuto: String(data.getUTCMinutes()).padStart(2, '0'),
  }
}

export function paraDataLocal(valor: string) {
  const data = new Date(valor)
  return new Date(
    data.getUTCFullYear(),
    data.getUTCMonth(),
    data.getUTCDate(),
    data.getUTCHours(),
    data.getUTCMinutes(),
  )
}

export function formatarDataHora(valor: string) {
  const { dia, mes, hora, minuto } = partes(valor)
  return `${dia}/${mes} ${hora}:${minuto}`
}

export function formatarDiaMes(dataIso: string) {
  const [, mes, dia] = dataIso.split('-')
  return `${dia}/${mes}`
}

export function formatarDataEHora(dataIso: string, hora: string) {
  const [ano, mes, dia] = dataIso.split('-')
  return `${dia}/${mes}/${ano} ${hora.slice(0, 5)}`
}

export function formatarPermanencia(entrada: string, saida: string) {
  return formatarDuracao((Date.parse(saida) - Date.parse(entrada)) / 60000)
}

export function formatarMoeda(valor: number) {
  return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

export function dataDeHoje() {
  const agora = new Date()
  const mes = String(agora.getMonth() + 1).padStart(2, '0')
  const dia = String(agora.getDate()).padStart(2, '0')
  return `${agora.getFullYear()}-${mes}-${dia}`
}

export function formatarHora(valor: string) {
  const { hora, minuto } = partes(valor)
  return `${hora}:${minuto}`
}

export function formatarDuracao(minutosTotais: number) {
  const minutos = Math.max(0, Math.round(minutosTotais))
  return `${Math.floor(minutos / 60)}h ${String(minutos % 60).padStart(2, '0')}min`
}
