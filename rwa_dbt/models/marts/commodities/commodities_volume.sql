{{ config(
    materialized='table'
) }}

-- Aggregate daily transfer volumes by stablecoin

SELECT 
  date,
  SUM(CASE WHEN asset_id = 246516580 THEN daily_volume ELSE 0 END) AS volume_246516580_GOLD$,
  SUM(CASE WHEN asset_id = 246519683 THEN daily_volume ELSE 0 END) AS volume_246519683_SILVER$,
  SUM(CASE WHEN asset_id = 1241944285 THEN daily_volume ELSE 0 END) AS volume_1241944285_Gold
FROM {{ ref('int_commodities_volumes') }}
GROUP BY date
ORDER BY date
