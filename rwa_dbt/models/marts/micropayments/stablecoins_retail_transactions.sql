-- models/marts/adjusted_transactions.sql
{{ config(
    materialized='table',
    tags=['rwa_retail_stablecoins']
) }}

SELECT *
FROM {{ ref('retail_adjusted_transactions') }}
ORDER BY realtime
