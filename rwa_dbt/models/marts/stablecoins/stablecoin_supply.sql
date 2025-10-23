{{ config(
    materialized='table'
) }}

SELECT 
  *
FROM {{ ref('int_stablecoin_supply') }}
ORDER BY date
