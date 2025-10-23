ADDRESSES = """
WITH all_users AS (
  SELECT
    toStartOfMonth(realtime) AS date,
    rcv_addr_id as id,
    'mann' AS tx_type
  FROM mainnet.txn
  WHERE snd_addr_id = 9401368139
  AND type_ext = 'asa_transfer'
  
  UNION ALL
  
  SELECT
    toStartOfMonth(realtime) AS date,
    snd_addr_id as id,
    'labtrace' AS tx_type
  FROM mainnet.txn
  WHERE asset_id = 1202296675
),
monthly_counts AS (
SELECT 
  date,
  uniqIf(id, tx_type = 'mann') AS MannDeshi,
  uniqIf(id, tx_type = 'labtrace') AS LabTrace,
  uniq(id) AS total_unique_addresses
FROM all_users
GROUP BY date
ORDER BY date
),
with_cumulative AS (
  SELECT 
    date,
    MannDeshi,
    LabTrace,
    total_unique_addresses,
    sum(total_unique_addresses) OVER (ORDER BY date) AS cumulative_users
  FROM monthly_counts
)
SELECT *
FROM with_cumulative
WHERE date >= toStartOfMonth(today() - INTERVAL 12 MONTH)
ORDER BY date
"""

CERTIFICATES = """
WITH all_transactions AS (
  SELECT
    toStartOfMonth(created_at_rt) AS date,
    id as id,
    'mann' AS tx_type
  FROM mainnet.asset
  WHERE creator_addr_id = 9401368139
  
  UNION ALL
  
  SELECT
    toStartOfMonth(created_at_rt) AS date,
    id,
    'labtrace' AS tx_type
  FROM mainnet.asset
  WHERE name like 'LT-%'
),
monthly_counts AS (
  SELECT 
    date,
    uniqIf(id, tx_type = 'mann') AS MannDeshi,
    uniqIf(id, tx_type = 'labtrace') AS LabTrace,
    uniq(id) AS total_certificates
  FROM all_transactions
  GROUP BY date
),
with_cumulative AS (
  SELECT 
    date,
    MannDeshi,
    LabTrace,
    total_certificates,
    sum(total_certificates) OVER (ORDER BY date) AS cumulative_certificates
  FROM monthly_counts
)
SELECT *
FROM with_cumulative
WHERE date >= toStartOfMonth(today() - INTERVAL 12 MONTH)
ORDER BY date
"""
