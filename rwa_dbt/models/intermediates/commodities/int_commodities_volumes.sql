{{ config(
    materialized='incremental',
    unique_key=['date', 'asset_id'],
    incremental_strategy='delete+insert'
) }}

-- Compute daily transfer volume per stablecoin

SELECT 
  toDate(realtime) AS date,
  asset_id,
  CASE 
    WHEN asset_id = 246516580 THEN 'GOLD$'
    WHEN asset_id = 246519683 THEN 'SILVER$'
    WHEN asset_id = 1241944285 THEN 'Gold'
  END AS asset,
  SUM(amount) / 1e6 AS daily_volume
FROM {{ ref('stg_commodities_txn') }}
WHERE type_ext = 'asa_transfer'
{% if is_incremental() %}
  AND toDate(realtime) >= date_sub(day, 7, today())
{% endif %}
GROUP BY date, asset_id, asset
