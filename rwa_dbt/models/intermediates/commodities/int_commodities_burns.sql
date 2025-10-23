{{ config(materialized='table') }}

WITH burn_wallets AS (
  SELECT arrayJoin([
    273563010, 273563012, 273563013, 3592797214, 3592787852, 273563011, -- meld
    3555067447 -- asa
  ]) AS wallet_id
)

SELECT 
  toStartOfMonth(realtime) AS date,
  t.asset_id,
  CASE 
    WHEN t.asset_id = 246516580 THEN 'GOLD$'
    WHEN t.asset_id = 246519683 THEN 'SILVER$'
    WHEN t.asset_id = 1241944285 THEN 'Gold'
  END AS asset,
  SUM(t.amount) / 1e6 AS burns
FROM mainnet.txn AS t
JOIN burn_wallets bw ON t.rcv_addr_id = bw.wallet_id
WHERE t.asset_id IN (246516580, 246519683, 1241944285)
  AND t.snd_addr_id NOT IN (SELECT wallet_id FROM burn_wallets)
GROUP BY date, asset_id, asset
ORDER BY date, asset_id
