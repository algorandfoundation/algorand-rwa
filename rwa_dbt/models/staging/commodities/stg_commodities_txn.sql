{{ config(
    materialized='view'
) }}

SELECT
  toDate(realtime) AS date,
  realtime,
  snd_addr_id,
  rcv_addr_id,
  asset_id,
  type_ext,
  amount
FROM mainnet.txn
WHERE asset_id IN (246516580, 246519683, 1241944285)
