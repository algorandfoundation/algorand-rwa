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

MARKET_VOLUME = """
WITH
rounds_with_lofty_swaps AS (
    SELECT DISTINCT round AS rnd
    FROM mainnet.txn
    WHERE app_id IN (
            SELECT id AS contract_id
            FROM mainnet.app
            WHERE creator_addr_id = 2402554280
        )
      AND has_inners
      AND realtime >= '2022-09-13'
),
lofty_swap_intras AS (
    SELECT
        t1.round,
        tt.intra AS inner_intra,
        tt.parent AS parent_intra,
        t1.realtime,
        t1.txid,
        t1.type_ext AS parent_type,
        t1.app_id,
        t2.type_ext AS child_type,
        t2.asset_id,
        t2.amount
    FROM mainnet.txn AS t1
    INNER JOIN mainnet.txntree AS tt
        ON t1.round = tt.round
       AND t1.intra = tt.parent
    INNER JOIN mainnet.txn AS t2
        ON t1.round = t2.round
       AND t2.intra = tt.intra
    WHERE t1.realtime >= '2022-09-13'
      AND t1.round IN (SELECT rnd FROM rounds_with_lofty_swaps)
      AND t1.app_id IN (
            SELECT id AS contract_id
            FROM mainnet.app
            WHERE creator_addr_id = 2402554280
        )
      AND t1.has_inners
      AND t2.asset_id = 31566704
      AND tt.intra = tt.parent + 1
      AND JSONExtract(t1.txn_extra, 'apaa', 'Array(String)')[1] = 'U3dhcA=='
      AND JSONExtract(t1.txn_extra, 'apas', 'Array(String)')[1] = '31566704'
    SETTINGS join_algorithm = 'full_sorting_merge'
),
monthly_volumes AS (
    SELECT
        toStartOfMonth(toDate(t1.realtime)) AS month_date,
        sum(toFloat64(t2.amount)) / 1e6 AS monthly_volume
    FROM lofty_swap_intras
    GROUP BY month_date
),
month_bounds AS (
    SELECT
        min(month_date) AS min_month,
        toStartOfMonth(today()) AS max_month
    FROM monthly_volumes
),
month_spine AS (
    SELECT arrayJoin(
        arrayMap(
            i -> addMonths((SELECT min_month FROM month_bounds), i),
            range(
                dateDiff('month', (SELECT min_month FROM month_bounds), (SELECT max_month FROM month_bounds)) + 1
            )
        )
    ) AS month_date
),
complete_monthly AS (
    SELECT
        ms.month_date,
        coalesce(mv.monthly_volume, 0) AS monthly_volume
    FROM month_spine AS ms
    LEFT JOIN monthly_volumes AS mv ON ms.month_date = mv.month_date
),
cumulative AS (
    SELECT
        month_date,
        monthly_volume,
        sum(monthly_volume) OVER (
            ORDER BY month_date ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_market_volume
    FROM complete_monthly
)
SELECT
    month_date AS month,
    monthly_volume AS market_volume,
    cumulative_market_volume
FROM cumulative
WHERE month_date >= addMonths(toStartOfMonth(today()), -12)
ORDER BY month_date ASC
"""

AMM_BUY = """
WITH rounds_with_lofty_swaps AS (
    SELECT DISTINCT round AS rnd
    FROM mainnet.txn
    WHERE realtime >= '2023-12-08'
      AND positionCaseInsensitive(reinterpretAsString(base64Decode(note)), 'loftyamm-') > 0
),
buy_amts as (
SELECT 
    t1.realtime AS realtime,
    sum(
        toFloat64(
            JSONExtractInt(
                JSONExtractRaw(
                    JSONExtractRaw(reinterpretAsString(base64Decode(t1.note)), 'data'),
                    'meta'
                ),
                'amount'
            )
        )
    ) / 1e6 AS buy_amt
FROM mainnet.txn t1
WHERE 
    t1.realtime >= '2023-12-08'
    AND t1.round IN (SELECT rnd FROM rounds_with_lofty_swaps)
    AND t1.note IS NOT NULL
    AND positionCaseInsensitive(reinterpretAsString(base64Decode(t1.note)), 'loftyamm-') > 0
  AND JSONExtractString(
      JSONExtractRaw(reinterpretAsString(base64Decode(t1.note)), 'data'),
                                                                'method'
                                                            ) = 'AssetTransferTxn'
  AND JSONExtractInt(
      JSONExtractRaw(JSONExtractRaw(reinterpretAsString(base64Decode(t1.note)), 'data'),
                                                                                'meta'
                                                                            ),
                                                                            'assetId'
                                                                        ) = 31566704
GROUP BY realtime
ORDER BY realtime ASC
),
monthly_buy AS (
    SELECT
        toStartOfMonth(realtime) AS month,
        sum(buy_amt) AS monthly_buy_volume
    FROM buy_amts
    GROUP BY month
),
monthly_cumulative AS (
    SELECT
        month,
        monthly_buy_volume,
        sum(monthly_buy_volume) OVER (
            ORDER BY month ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_buy_volume
    FROM monthly_buy
)
SELECT
    month,
    monthly_buy_volume,
    cumulative_buy_volume
FROM monthly_cumulative
WHERE month >= addMonths(toStartOfMonth(today()), -12)
ORDER BY month ASC
"""

AMM_SELL = """
WITH rounds_with_lofty_swaps AS (
    SELECT DISTINCT round AS rnd,
          realtime,
          intra
    FROM mainnet.txn
    WHERE realtime >= '2023-12-08'
      AND has_inners 
      AND positionCaseInsensitive(reinterpretAsString(base64Decode(note)), 'loftyamm-') > 0
      AND JSONExtractString(
      JSONExtractRaw(reinterpretAsString(base64Decode(note)), 'data'),
                                                                'method'
                                                            ) = 'sell_base_token'
),
sell_amts as (
select 
        t1.rnd,
       -- tt.intra inner_intra,
        --tt.parent parent_intra,
        t1.realtime as realtime,
        t2.txid,
        t2.type_ext,
        t2.asset_id,
        t2.amount/1e6 as sell_amt
    from rounds_with_lofty_swaps t1
    --join mainnet.txntree tt on (t1.round = tt.round and t1.intra = tt.parent) 
    join mainnet.txn t2 on (t1.rnd = t2.round and t2.intra = t1.intra+2)
    where 
     t1.rnd in (select rnd from rounds_with_lofty_swaps)
    and t2.asset_id = 31566704
    AND t2.amount >0
    settings join_algorithm = 'full_sorting_merge'    
),
monthly_sell AS (
    SELECT
        toStartOfMonth(realtime) AS month,
        sum(sell_amt) AS monthly_sell_volume
    FROM sell_amts
    GROUP BY month
),
monthly_cumulative AS (
    SELECT
        month,
        monthly_sell_volume,
        sum(monthly_sell_volume) OVER (
            ORDER BY month ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_sell_volume
    FROM monthly_sell
)
SELECT
    month,
    monthly_sell_volume,
    cumulative_sell_volume
FROM monthly_cumulative
WHERE month >= addMonths(toStartOfMonth(today()), -12)
ORDER BY month ASC
"""