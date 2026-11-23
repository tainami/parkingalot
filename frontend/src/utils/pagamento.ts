export const TARIFA_POR_HORA = 3
export const MINUTOS_GRATIS = 30

export function calcularValorEstimado(minutos: number) {
  const minutosCobrados = Math.max(0, minutos - MINUTOS_GRATIS)
  return Math.round(((TARIFA_POR_HORA / 60) * minutosCobrados) * 100) / 100
}
