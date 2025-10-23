{{ config(materialized='table') }}

WITH burn_wallets AS (
  SELECT arrayJoin([
    334314076, 337849393, 337846447, 345003642, 345005068, -- USDC
    138399456, -- USDT
    1445874475, 1332138752, 3042324867, -- GOUSD
    1355935955, 2741347927, 2853884730, 4015457176 -- XUSD
  ]) AS wallet_id
)

SELECT 
  toStartOfMonth(realtime) AS date,
  t.asset_id,
  CASE 
    WHEN t.asset_id = 31566704 THEN 'USDC'
    WHEN t.asset_id = 312769 THEN 'USDT'
    WHEN t.asset_id = 760037151 THEN 'XUSD'
    WHEN t.asset_id = 672913181 THEN 'GOUSD'
  END AS asset,
  SUM(t.amount) / 1e6 AS burns
FROM mainnet.txn AS t
JOIN burn_wallets bw ON t.rcv_addr_id = bw.wallet_id
WHERE t.asset_id IN (31566704, 312769, 760037151, 672913181)
  AND t.snd_addr_id NOT IN (SELECT wallet_id FROM burn_wallets)
GROUP BY date, asset_id, asset
ORDER BY date, asset_id
