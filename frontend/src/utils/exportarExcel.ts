export interface ColunaExcel<T> {
  titulo: string
  valor: (linha: T) => string | number
  largura?: number
}

export async function exportarExcel<T>(
  nomeArquivo: string,
  nomeAba: string,
  colunas: ColunaExcel<T>[],
  linhas: T[],
) {
  const { Workbook } = await import('exceljs')

  const planilha = new Workbook()
  const aba = planilha.addWorksheet(nomeAba)

  aba.columns = colunas.map((coluna) => ({
    header: coluna.titulo,
    width: coluna.largura ?? Math.max(12, coluna.titulo.length + 4),
  }))

  linhas.forEach((linha) => aba.addRow(colunas.map((coluna) => coluna.valor(linha))))

  const cabecalho = aba.getRow(1)
  cabecalho.font = { bold: true, color: { argb: 'FFFFFFFF' } }
  cabecalho.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF1E6FD9' } }
  aba.views = [{ state: 'frozen', ySplit: 1 }]

  const buffer = await planilha.xlsx.writeBuffer()
  const url = URL.createObjectURL(
    new Blob([buffer], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    }),
  )

  const link = document.createElement('a')
  link.href = url
  link.download = `${nomeArquivo}.xlsx`
  link.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}
