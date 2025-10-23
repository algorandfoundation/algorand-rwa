ACTIVE_WALLETS = """

WITH all_transactions AS (
  SELECT
    toStartOfMonth(realtime) AS date,
    snd_addr_id,
    'algo' AS tx_type
  FROM c_algorand.algo_retail_transactions
  
  UNION ALL
  
  SELECT
    toStartOfMonth(realtime) AS date,
    snd_addr_id,
    'stable' AS tx_type
  FROM c_algorand.stablecoins_retail_transactions
  
  UNION ALL
  
  SELECT
    toStartOfMonth(realtime) AS date,
    snd_addr_id,
    'hafn' AS tx_type
  FROM mainnet.txn 
  WHERE toDate(realtime) BETWEEN today() - INTERVAL 12 MONTH AND today()
    AND asset_id = 849191641
    AND type_ext = 'asa_transfer'
)
SELECT 
  date,
  uniqIf(snd_addr_id, tx_type = 'algo') AS algo_addresses,
  uniqIf(snd_addr_id, tx_type = 'stable') AS stable_addresses,
  uniqIf(snd_addr_id, tx_type = 'hafn') AS hafn_addresses,
  uniq(snd_addr_id) AS total_unique_addresses
FROM all_transactions
GROUP BY date
ORDER BY date
"""

TRANSACTIONS = """
SELECT 
  COALESCE(a.date, s.date, h.date) AS date,
  COALESCE(a.algo_transactions, 0) AS algo_transactions,
  COALESCE(s.stable_transactions, 0) AS stable_transactions,
  COALESCE(h.hafn_transactions, 0) AS hafn_transactions,
  COALESCE(a.algo_transactions, 0) + COALESCE(s.stable_transactions, 0) + COALESCE(h.hafn_transactions, 0) AS total_transactions
FROM (
  SELECT
    toDate(realtime) AS date, 
    count(*) AS algo_transactions
  FROM c_algorand.algo_retail_transactions
  GROUP BY date
) a
FULL OUTER JOIN (
  SELECT
    toDate(realtime) AS date, 
    count(*) AS stable_transactions
  FROM c_algorand.stablecoins_retail_transactions
  GROUP BY date
) s ON a.date = s.date
FULL OUTER JOIN (
  SELECT
    toDate(realtime) AS date,
    count(*) AS hafn_transactions
  FROM mainnet.txn 
  WHERE toDate(realtime) BETWEEN today() - INTERVAL 12 MONTH AND today()
    AND asset_id = 849191641
    AND type_ext = 'asa_transfer'
  GROUP BY date
) h ON COALESCE(a.date, s.date) = h.date
ORDER BY date
"""

VOLUME_1 = """
SELECT 
  COALESCE(a.date, s.date) AS date,
  COALESCE(a.algo_vol, 0) AS algo_vol,
  COALESCE(s.stable_vol, 0) AS stable_vol,
  COALESCE(a.algo_vol, 0) + COALESCE(s.stable_vol, 0) AS total_vol
FROM (
  SELECT
    toDate(realtime) AS date, 
    sum(usd_amount) AS algo_vol
  FROM c_algorand.algo_retail_transactions
  GROUP BY date
) a
FULL OUTER JOIN (
  SELECT
    toDate(realtime) AS date, 
    sum(amount)/1e6 AS stable_vol
  FROM c_algorand.stablecoins_retail_transactions
  GROUP BY date
) s ON a.date = s.date
 ORDER BY date
"""

VOLUME_2 = """
SELECT
    toDate(realtime) AS date,
    sum(amount)/1e6 AS hafn_vol
FROM mainnet.txn 
WHERE toDate(realtime) BETWEEN today() - INTERVAL 12 MONTH AND today()
    AND asset_id = 849191641
    AND type_ext = 'asa_transfer'
GROUP BY date
ORDER BY date
"""
