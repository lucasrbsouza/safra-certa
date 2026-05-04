from dataclasses import dataclass


@dataclass
class CostBreakdown:
    seeds: float
    fertilizers: float
    defensivos: float
    labor: float
    fuel: float
    maintenance: float

    def total(self) -> float:
        return self.seeds + self.fertilizers + self.defensivos + self.labor + self.fuel + self.maintenance


@dataclass
class SimulationResult:
    crop_type: str
    total_cost_per_hectare: float
    market_price_per_sack: float
    breakeven_sacks_per_hectare: float
    estimated_productivity: float
    profit_loss_per_hectare: float
    is_viable: bool
    currency: str = "BRL"
