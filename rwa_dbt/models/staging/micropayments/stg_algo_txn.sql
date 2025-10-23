-- models/staging/stg_mainnet_txn.sql
{{ config(materialized='view') }}

WITH daily_pool_rates AS (
  SELECT 
    toDate(realtime) AS date,
    argMax(pool_rate, realtime) AS pool_rate  -- Gets the last pool_rate for each date
  FROM mainnet.v_swaps_tm2
  WHERE pool_token_asa_id = 1002590888
        and toDate(realtime) BETWEEN today() - INTERVAL 12 MONTH AND today()
  GROUP BY toDate(realtime)
)
SELECT 
  t.realtime,
  t.snd_addr_id,
  t.amount,
  r.pool_rate,
  r.pool_rate * t.amount / 1e6 AS usd_amount
FROM mainnet.txn t
INNER JOIN daily_pool_rates r ON toDate(t.realtime) = r.date
WHERE toDate(t.realtime) BETWEEN today() - INTERVAL 12 MONTH AND today()
  AND t.type_ext = 'acc_payment'
  AND t.amount > 1000
  AND r.pool_rate * t.amount / 1e6 <= 250

ORDER BY t.realtime
