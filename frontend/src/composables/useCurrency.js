const formatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
  minimumFractionDigits: 2,
})

export function useCurrency() {
  function formatBRL(value) {
    if (value === null || value === undefined) return '–'
    return formatter.format(Number(value))
  }

  function formatSacks(value) {
    if (value === null || value === undefined) return '–'
    return `${Number(value).toLocaleString('pt-BR', { maximumFractionDigits: 2 })} sc/ha`
  }

  return { formatBRL, formatSacks }
}
