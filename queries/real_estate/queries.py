PROPERTIES = """
WITH first_seen_tokens AS (
    -- Get each token's first appearance month
    SELECT
        unit_name,
        toStartOfMonth(min(created_at_rt)) AS first_seen_month
    FROM mainnet.asset
    WHERE creator_addr_id = 952362238
      AND unit_name LIKE 'LFTY%'
      AND not deleted
    GROUP BY unit_name
),

monthly_counts AS (
    -- Aggregate tokens created each month
    SELECT
        first_seen_month AS month_date,
        count() AS monthly_tokenized
    FROM first_seen_tokens
    GROUP BY first_seen_month
),

bounds AS (
    -- Get date bounds to build full month spine
    SELECT
        toStartOfMonth(min(first_seen_month)) AS min_month,
        toStartOfMonth(today()) AS max_month
    FROM first_seen_tokens
),

month_spine AS (
    -- Generate a continuous list of months
    SELECT
        arrayJoin(
            arrayMap(
                i -> addMonths((SELECT min_month FROM bounds), i),
                range(
                    dateDiff('month', (SELECT min_month FROM bounds), (SELECT max_month FROM bounds)) + 1
                )
            )
        ) AS month_date
),

final AS (
    -- Join the month spine with real data, fill gaps with zeros
    SELECT
        ms.month_date,
        coalesce(mc.monthly_tokenized, 0) AS monthly_tokenized,
        sum(coalesce(mc.monthly_tokenized, 0)) OVER (
            ORDER BY ms.month_date ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_tokenized
    FROM month_spine ms
    LEFT JOIN monthly_counts mc
        ON ms.month_date = mc.month_date
)

-- Filter to the last 6 months
SELECT
    month_date,
    monthly_tokenized,
    cumulative_tokenized
FROM final
WHERE month_date BETWEEN dateTrunc('month', addMonths(today(), -6))
                     AND dateTrunc('month', today())
ORDER BY month_date ASC
"""

MARKET_CAP = """
WITH
-- Tokens created by the treasury
tokens AS (
    SELECT
        unit_name AS unique_token_id
    FROM mainnet.asset
    WHERE creator_addr_id = 952362238
      AND unit_name LIKE 'LFTY%'
),

-- Reserve addresses for exclusion
reserves AS (
    SELECT DISTINCT reserve_addr_id
    FROM mainnet.asset
    WHERE creator_addr_id = 952362238
      AND unit_name LIKE 'LFTY%'
),

-- Daily mint and burn net supply changes
daily_mint_burn AS (
    SELECT
        toDate(realtime) AS date,
        SUM(
            CASE
                WHEN snd_addr_id = 952362238
                     AND rcv_addr_id NOT IN (
                         SELECT reserve_addr_id FROM reserves
                     )
                    THEN toFloat64(amount)  -- Mint (tokens leaving treasury)
                WHEN rcv_addr_id = 952362238
                    THEN -toFloat64(amount) -- Burn (tokens returning to treasury)
                ELSE 0
            END
        ) AS daily_net_supply_change
    FROM mainnet.txn
    WHERE (snd_addr_id = 952362238 OR rcv_addr_id = 952362238)
      AND asset_unit_name IN (
          SELECT unique_token_id FROM tokens
      )
      AND realtime IS NOT NULL
    GROUP BY toDate(realtime)
),

-- Determine date range bounds
date_bounds AS (
    SELECT
        min(date) AS min_date,
        today() AS max_date
    FROM daily_mint_burn
),

-- Generate continuous daily date spine
date_range AS (
    SELECT
        arrayJoin(
            arrayMap(
                i -> addDays((SELECT min_date FROM date_bounds), i),
                range(
                    dateDiff(
                        'day',
                        (SELECT min_date FROM date_bounds),
                        (SELECT max_date FROM date_bounds)
                    ) + 1
                )
            )
        ) AS date
),

-- Fill missing dates with zeros
complete_daily_data AS (
    SELECT
        dr.date,
        coalesce(dmb.daily_net_supply_change, 0) AS daily_net_supply_change
    FROM date_range AS dr
    LEFT JOIN daily_mint_burn AS dmb
        ON dr.date = dmb.date
),

-- Compute cumulative supply
cumulative_supply AS (
    SELECT
        date,
        daily_net_supply_change,
        sum(daily_net_supply_change)
            OVER (ORDER BY date ASC
                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
            AS cumulative_supply_change
    FROM complete_daily_data
)

-- Final result
SELECT
    date,
    cumulative_supply_change,
    cumulative_supply_change * 50 AS market_cap
FROM cumulative_supply
WHERE cumulative_supply_change > 0
  AND date BETWEEN addMonths(toDate(today()), -6) AND toDate(today())
ORDER BY date ASC
"""


ACTIVE_WALLETS = """
WITH 
-- Market apps (created or used by the treasury)
market_apps AS (
    SELECT DISTINCT app_id AS id
    FROM mainnet.txn
    WHERE snd_addr_id = 3623345007

    UNION ALL

    SELECT id
    FROM mainnet.app
    WHERE creator_addr_id = 2402554280
),

-- User first appearance
user_first_appearance AS (
    SELECT
        snd_addr_id AS user_id,
        toStartOfMonth(toDate(min(realtime))) AS first_month
    FROM mainnet.txn
    WHERE app_id IN (SELECT id FROM market_apps)
      AND toDate(realtime) >= '2022-09-13'
    GROUP BY snd_addr_id
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
WHERE month >= addMonths(toStartOfMonth(today()), -6)
ORDER BY month ASC
"""