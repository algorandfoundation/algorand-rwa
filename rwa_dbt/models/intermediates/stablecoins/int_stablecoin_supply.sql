{{ config(materialized='table') }}

SELECT
  date,
  SUM(CASE WHEN asset_id = 31566704 THEN circulating_supply ELSE 0 END) AS supply_31566704_USDC,
  SUM(CASE WHEN asset_id = 312769 THEN circulating_supply ELSE 0 END) AS supply_312769_USDT,
  SUM(CASE WHEN asset_id = 760037151 THEN circulating_supply ELSE 0 END) AS supply_760037151_XUSD,
  SUM(CASE WHEN asset_id = 672913181 THEN circulating_supply ELSE 0 END) AS supply_672913181_GOUSD,
  SUM(COALESCE(circulating_supply, 0)) AS total_circulating_supply
FROM {{ ref('int_stablecoin_daily_changes') }}
GROUP BY date
ORDER BY date
