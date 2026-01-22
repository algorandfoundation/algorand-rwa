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
    WHEN asset_id = 31566704 THEN 'USDC'
    WHEN asset_id = 312769 THEN 'USDT'
    WHEN asset_id = 760037151 THEN 'XUSD'
    WHEN asset_id = 672913181 THEN 'GOUSD'
  END AS asset,
  SUM(amount) / 1e6 AS daily_volume
FROM {{ ref('stg_stablecoin_txn') }}
WHERE type_ext = 'asa_transfer'
{% if is_incremental() %}
  AND toDate(realtime) >= date_sub(day, 7, today())
{% endif %}
GROUP BY date, asset_id, asset
