{{ config(materialized='table') }}

SELECT
  date,
  SUM(CASE WHEN asset_id = 246516580 THEN circulating_supply ELSE 0 END) AS supply_246516580_GOLD$,
  SUM(CASE WHEN asset_id = 246519683 THEN circulating_supply ELSE 0 END) AS supply_246519683_SILVER$,
  SUM(CASE WHEN asset_id = 1241944285 THEN circulating_supply ELSE 0 END) AS supply_1241944285_Gold,
  SUM(COALESCE(circulating_supply, 0)) AS total_circulating_supply
FROM {{ ref('int_commodities_daily_changes') }}
GROUP BY date
ORDER BY date
