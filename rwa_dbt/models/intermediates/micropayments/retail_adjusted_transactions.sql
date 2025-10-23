-- models/intermediate/int_adjusted_transactions.sql
{{ config(materialized='ephemeral') }}

SELECT 
  t.realtime,
  t.snd_addr_id,
  t.amount
FROM {{ ref('stg_mainnet_txn') }} t
LEFT JOIN {{ ref('retail_address_stats') }} stats 
  ON t.snd_addr_id = stats.snd_addr_id
WHERE toDate(t.realtime) BETWEEN today() - INTERVAL 12 MONTH AND today()
  AND t.type_ext = 'asa_transfer'
  AND (
    stats.max_tx_count_30d <= 1000 OR isNull(stats.max_tx_count_30d)
  )
  AND (
    stats.max_volume_30d <= 10000000 * 1000000 OR isNull(stats.max_volume_30d)
  )
  AND t.amount / 1e6 <= 250
