{{ config(
    materialized='table'
) }}

-- Aggregate daily transfer volumes by stablecoin

SELECT 
  date,
  SUM(CASE WHEN asset_id = 31566704 THEN daily_volume ELSE 0 END) AS volume_31566704_USDC,
  SUM(CASE WHEN asset_id = 312769 THEN daily_volume ELSE 0 END) AS volume_312769_USDT,
  SUM(CASE WHEN asset_id = 760037151 THEN daily_volume ELSE 0 END) AS volume_760037151_XUSD,
  SUM(CASE WHEN asset_id = 672913181 THEN daily_volume ELSE 0 END) AS volume_672913181_GOUSD,
  SUM(COALESCE(daily_volume, 0)) AS total_stablecoin_volume
FROM {{ ref('int_stablecoin_volumes') }}
GROUP BY date
ORDER BY date
