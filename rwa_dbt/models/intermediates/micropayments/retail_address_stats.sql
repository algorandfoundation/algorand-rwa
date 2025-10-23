-- models/intermediate/int_address_stats.sql
{{ config(materialized='ephemeral') }}

SELECT 
  snd_addr_id,
  MAX(tx_count_30d) AS max_tx_count_30d,
  MAX(volume_30d) AS max_volume_30d
FROM (
  SELECT 
    snd_addr_id,
    COUNT(*) OVER (
      PARTITION BY snd_addr_id 
      ORDER BY toUnixTimestamp(realtime)
      RANGE BETWEEN 2592000 PRECEDING AND CURRENT ROW
    ) AS tx_count_30d,
    SUM(amount) OVER (
      PARTITION BY snd_addr_id 
      ORDER BY toUnixTimestamp(realtime)
      RANGE BETWEEN 2592000 PRECEDING AND CURRENT ROW
    ) AS volume_30d
  FROM {{ ref('stg_mainnet_txn') }}
)
GROUP BY snd_addr_id
