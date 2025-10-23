-- models/marts/adjusted_transactions.sql
{{ config(
    materialized='table',
    tags=['rwa_retail_stablecoins']
) }}

SELECT *
FROM {{ ref('stg_algo_txn') }}
ORDER BY realtime
