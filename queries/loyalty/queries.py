ADDRESSES = """
WITH 

-- User first appearance
user_first_appearance AS (
    SELECT
        rcv_addr_id AS user_id,
        toStartOfMonth(toDate(min(realtime))) AS first_month
    FROM mainnet.txn
    WHERE asset_id = 3145862805
      AND type_ext = 'asa_transfer'
    GROUP BY rcv_addr_id
),

-- Monthly new users (how many first appeared that month)
monthly_new_users AS (
    SELECT
        first_month AS month,
        countDistinct(user_id) AS new_users
    FROM user_first_appearance
    GROUP BY first_month
),

-- Month bounds and spine
month_bounds AS (
    SELECT
        toStartOfMonth(min(first_month)) AS min_month,
        toStartOfMonth(max(first_month)) AS max_month
    FROM user_first_appearance
),

month_spine AS (
    SELECT arrayJoin(
        arrayMap(
            i -> addMonths((SELECT min_month FROM month_bounds), i),
            range(
                dateDiff('month', (SELECT min_month FROM month_bounds), (SELECT max_month FROM month_bounds)) + 1
            )
        )
    ) AS month
),

-- Join spine with actual new users (fill gaps)
monthly_users AS (
    SELECT
        ms.month,
        coalesce(mu.new_users, 0) AS new_users
    FROM month_spine AS ms
    LEFT JOIN monthly_new_users AS mu ON ms.month = mu.month
),

-- Compute cumulative users using window function
cumulative_users AS (
    SELECT
        month,
        new_users AS monthly_unique_users,
        sum(new_users) OVER (ORDER BY month ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
            AS cumulative_unique_users
    FROM monthly_users
)

-- Final output
SELECT
    month,
    monthly_unique_users,
    cumulative_unique_users
FROM cumulative_users
WHERE month >= addMonths(toStartOfMonth(today()), -12)
ORDER BY month ASC
"""

TRANSACTIONS = """
with wcpp_tx as (
SELECT toStartOfMonth(realtime) as month, 
       count(*) as txn 
FROM mainnet.txn
WHERE asset_id = 3145862805
GROUP BY month 
ORDER BY month
),
cumulatives as (
SELECT month, 
       txn, 
       sum(txn) OVER (ORDER BY month) as total_txn 
FROM wcpp_tx
)
SELECT *
FROM cumulatives 
WHERE month >= addMonths(toStartOfMonth(today()), -12)
ORDER BY month ASC
"""