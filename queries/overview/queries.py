TRANSACTIONS = """
WITH market_apps AS (
    SELECT app_id as id
    FROM mainnet.txn 
    WHERE snd_addr_id = 3623345007 --'YDYVLRLNZKOWGPARJVFMZLI4EFVXZD2A4ATNFW6AQEYLLP4AHFNBM7O3BU'
    
    UNION ALL
    
    SELECT id
    FROM mainnet.app
    WHERE creator_addr_id = 2402554280 -- LFTYNHQEOZYYIFFLPA246HYX3ZIPZHDL3GZTHHKQVJB6DQGHF2ZMB5QEEU
),
monthly_stats AS (
    SELECT
        toStartOfMonth(realtime) as mt,
        -- Lofty transactions and fees
        COUNT(CASE WHEN app_id IN (SELECT id FROM market_apps) THEN 1 END) as lofty_transactions,
        -- Other projects
        COUNT(CASE WHEN asset_id IN (1241944285) THEN 1 END) AS asa_gold,
        COUNT(CASE WHEN asset_id IN (246516580, 246519683) THEN 1 END) AS meld_gold,
        COUNT(CASE WHEN asset_id = 849191641 THEN 1 END) AS HAFN,
        COUNT(CASE WHEN asset_id IN (3145862805, 3145863799) THEN 1 END) AS world_chess,
        COUNT(CASE WHEN snd_addr_id = 9401368139 THEN 1 END) AS mann,
        COUNT(CASE WHEN asset_unit_name like 'LT-%' THEN 1 END) AS labtrace, 
        COUNT(CASE WHEN asset_id in (31566704, 312769, 760037151, 672913181) THEN 1 END) AS stables
    FROM mainnet.txn 
    GROUP BY mt
),
cumulatives as (
SELECT mt,
       (lofty_transactions+asa_gold+meld_gold+HAFN+world_chess+mann+labtrace+stables) as transactions,
       SUM(lofty_transactions+asa_gold+meld_gold+HAFN+world_chess+mann+labtrace+stables) OVER (ORDER BY mt) as total_transactions
FROM monthly_stats 
)
SELECT 
    *
FROM cumulatives
where mt >= toStartOfMonth(today() - INTERVAL 12 MONTH)
order by mt
"""

ACTIVE_WALLETS = """

WITH market_apps AS (
    SELECT app_id as id
    FROM mainnet.txn 
    WHERE snd_addr_id = 3623345007 --'YDYVLRLNZKOWGPARJVFMZLI4EFVXZD2A4ATNFW6AQEYLLP4AHFNBM7O3BU'
    
    UNION ALL
    
    SELECT id
    FROM mainnet.app
    WHERE creator_addr_id = 2402554280 -- LFTYNHQEOZYYIFFLPA246HYX3ZIPZHDL3GZTHHKQVJB6DQGHF2ZMB5QEEU
),
-- Get first time each wallet used any RWA service
wallet_first_seen AS (
    SELECT 
        COALESCE(snd_addr_id, rcv_addr_id) as wallet_id,
        MIN(toStartOfMonth(realtime)) as first_month
    FROM mainnet.txn
    WHERE 
        app_id IN (SELECT id FROM market_apps)
        OR asset_id IN (1241944285, 246516580, 246519683, 849191641, 3145862805, 3145863799, 31566704, 312769, 760037151, 672913181)
        OR snd_addr_id = 9401368139
        OR asset_unit_name LIKE 'LT-%'
    GROUP BY COALESCE(snd_addr_id, rcv_addr_id)
),
-- Count cumulative wallets by their first seen month
cumulative_wallets AS (
    SELECT 
        first_month as mt,
        COUNT(DISTINCT wallet_id) as new_wallets_count
    FROM wallet_first_seen
    GROUP BY first_month
),
monthly_stats AS (
    SELECT
        toStartOfMonth(realtime) as mt,
        -- Lofty transactions and fees
        COUNT(DISTINCT CASE WHEN app_id IN (SELECT id FROM market_apps) THEN snd_addr_id END) as lofty_wallets,
        -- Other projects
        COUNT(DISTINCT CASE WHEN asset_id IN (1241944285) THEN snd_addr_id END) AS asa_gold_wallets,
        COUNT(DISTINCT CASE WHEN asset_id IN (246516580, 246519683) THEN snd_addr_id END) AS meld_gold_wallets,
        COUNT(DISTINCT CASE WHEN asset_id = 849191641 THEN snd_addr_id END) AS HAFN_wallets,
        COUNT(DISTINCT CASE WHEN asset_id IN (3145862805, 3145863799) THEN rcv_addr_id END) AS world_chess_wallets,
        COUNT(DISTINCT CASE WHEN snd_addr_id = 9401368139 THEN rcv_addr_id END) AS mann_wallets,
        COUNT(DISTINCT CASE WHEN asset_unit_name LIKE 'LT-%' THEN snd_addr_id END) AS labtrace_wallets, 
        COUNT(DISTINCT CASE WHEN asset_id IN (31566704, 312769, 760037151, 672913181) THEN snd_addr_id END) AS stables_wallets,
        -- Unique wallets across all categories (no double counting)
        COUNT(DISTINCT CASE 
            WHEN app_id IN (SELECT id FROM market_apps) 
                OR asset_id IN (1241944285, 246516580, 246519683, 849191641, 3145862805, 3145863799, 31566704, 312769, 760037151, 672913181)
                OR snd_addr_id = 9401368139
                OR asset_unit_name LIKE 'LT-%'
            THEN COALESCE(snd_addr_id, rcv_addr_id)
        END) AS unique_wallets
    FROM mainnet.txn 
    GROUP BY toStartOfMonth(realtime)
),
cumulatives AS (
    SELECT 
        ms.mt,
        ms.unique_wallets,
        -- Cumulative unique wallets (counting only first appearance)
        SUM(COALESCE(cw.new_wallets_count, 0)) OVER (ORDER BY ms.mt ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as cumulative_unique_wallets
    FROM monthly_stats ms
    LEFT JOIN cumulative_wallets cw ON cw.mt = ms.mt
)
SELECT 
    *
FROM cumulatives
WHERE mt >= toStartOfMonth(today() - INTERVAL 12 MONTH)
ORDER BY mt
"""


USDC_VOLUME = """
WITH usdc as (
SELECT toStartOfMonth(realtime) as mt,
       sum(amount)/1e6 as volume 
FROM mainnet.txn 
WHERE asset_id = 31566704
      and (snd_addr_id not in (334314076, 337849393, 337846447, 345003642, 345005068)
          or rcv_addr_id not in (334314076, 337849393, 337846447, 345003642, 345005068))
GROUP BY mt 
ORDER BY mt
),
cumulatives as (
SELECT mt, 
       volume,
       sum(volume) over (ORDER BY mt) as cumulative_volume
FROM usdc
)
SELECT * 
FROM cumulatives
WHERE mt >= toStartOfMonth(today() - INTERVAL 12 MONTH)
ORDER BY mt
"""