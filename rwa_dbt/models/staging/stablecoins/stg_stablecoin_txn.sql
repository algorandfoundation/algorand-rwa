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
WHERE asset_id IN (31566704, 312769, 760037151, 672913181)
