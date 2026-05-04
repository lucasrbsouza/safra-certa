CREATE TABLE IF NOT EXISTS cost_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    crop_type VARCHAR(20) NOT NULL,
    seeds NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    fertilizers NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    defensivos NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    labor NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    fuel NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    maintenance NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cost_entries_crop_type ON cost_entries (crop_type);

CREATE TABLE IF NOT EXISTS commodity_cache (
    id SERIAL PRIMARY KEY,
    crop_type VARCHAR(20) UNIQUE NOT NULL,
    price_per_sack NUMERIC(10, 2) NOT NULL,
    source VARCHAR(50) NOT NULL,
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_commodity_cache_crop_type ON commodity_cache (crop_type);
