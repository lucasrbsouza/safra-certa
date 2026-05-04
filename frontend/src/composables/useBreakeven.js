import { computed } from 'vue'
import { useSimulationStore } from '@/stores/simulationStore.js'
import { useCurrency } from './useCurrency.js'

export function useBreakeven() {
  const store = useSimulationStore()
  const { formatBRL, formatSacks } = useCurrency()

  const formattedBreakeven = computed(() =>
    store.result ? formatSacks(store.result.breakeven_sacks_per_hectare) : '–',
  )

  const formattedProfitLoss = computed(() =>
    store.result ? formatBRL(store.result.profit_loss_per_hectare) : '–',
  )

  const formattedTotalCost = computed(() =>
    store.result ? formatBRL(store.result.total_cost_per_hectare) : '–',
  )

  const formattedMarketPrice = computed(() =>
    store.result ? formatBRL(store.result.market_price_per_sack) : '–',
  )

  const gaugePercentage = computed(() => {
    if (!store.result) return 0
    const { estimated_productivity, breakeven_sacks_per_hectare } = store.result
    if (breakeven_sacks_per_hectare === 0) return 100
    return Math.min((estimated_productivity / breakeven_sacks_per_hectare) * 100, 150)
  })

  async function simulate(payload) {
    if (!payload.estimated_productivity || payload.estimated_productivity <= 0) {
      throw new Error('Produtividade estimada deve ser maior que zero.')
    }
    await store.runSimulation(payload)
  }

  return {
    result: computed(() => store.result),
    loading: computed(() => store.loading),
    error: computed(() => store.error),
    isViable: store.isViable,
    statusColor: store.statusColor,
    statusLabel: store.statusLabel,
    formattedBreakeven,
    formattedProfitLoss,
    formattedTotalCost,
    formattedMarketPrice,
    gaugePercentage,
    simulate,
  }
}
