{{ config(
    materialized='table'
) }}

-- Aggregate daily transfer volumes by stablecoin

SELECT 
  dateTrunc('month', realtime) as month,
  COUNT(distinct snd_addr_id) as active_wallets
FROM {{ ref('stg_stablecoin_txn') }}
GROUP BY month
ORDER BY month
