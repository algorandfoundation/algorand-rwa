-- models/staging/stg_mainnet_txn.sql
{{ config(materialized='view') }}

SELECT
  realtime,
  snd_addr_id,
  asset_id,
  type_ext,
  amount
FROM mainnet.txn
WHERE toDate(realtime) BETWEEN today() - INTERVAL 13 MONTH AND today()
  AND asset_id IN (31566704, 312769, 760037151, 672913181)
