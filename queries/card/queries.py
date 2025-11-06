ACTIVE_ADDRESSES = """
WITH address_first_seen AS (
    SELECT 
        snd_addr_id,
        MIN(toStartOfMonth(toDate(realtime))) as first_month
    FROM mainnet.txn
    WHERE rcv_addr_id = 6060125595
        AND asset_id = 31566704
    GROUP BY snd_addr_id
),
monthly_stats AS (
    SELECT 
        toStartOfMonth(toDate(realtime)) as month,
        COUNT(DISTINCT snd_addr_id) as monthly_active_addresses
    FROM mainnet.txn
    WHERE rcv_addr_id = 6060125595
        AND asset_id = 31566704
    GROUP BY month
),
new_addresses_per_month AS (
    SELECT 
        first_month as month,
        COUNT(*) as new_addresses
    FROM address_first_seen
    GROUP BY first_month
)
SELECT 
    ms.month,
    ms.monthly_active_addresses,
    SUM(nam.new_addresses) OVER (ORDER BY ms.month) as cumulative_unique_addresses
FROM monthly_stats ms
LEFT JOIN new_addresses_per_month nam ON ms.month = nam.month
WHERE ms.month >= addMonths(toStartOfMonth(today()), -12)
ORDER BY ms.month
"""

TOTAL_TXN = """
WITH monthly_txns as (
SELECT toStartOfMonth(realtime) as month,
       COUNT(*) as monthly_transactions
from mainnet.txn
where rcv_addr_id = 6060125595
    and asset_id = 31566704
GROUP by month 
ORDER BY month
), cumulatives as (
SELECT month,
       monthly_transactions, 
       sum(monthly_transactions) OVER (ORDER BY month) as cumulative_transactions
FROM monthly_txns
)
SELECT * 
FROM cumulatives 
WHERE month >= addMonths(toStartOfMonth(today()), -12)
ORDER by month
"""

VOLUME = """
WITH monthly_vol as (
SELECT toStartOfMonth(realtime) as month,
       sum(amount)/1e6 as monthly_volume
from mainnet.txn
where rcv_addr_id = 6060125595
    and asset_id = 31566704
GROUP by month 
ORDER BY month
), cumulatives as (
SELECT month,
       monthly_volume, 
       sum(monthly_volume) OVER (ORDER BY month) as cumulative_volume
FROM monthly_vol
)
SELECT * 
FROM cumulatives 
WHERE month >= addMonths(toStartOfMonth(today()), -12)
ORDER by month
"""

