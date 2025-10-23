{{ config(
    materialized='table'
) }}

SELECT 
  *
FROM {{ ref('int_commodities_supply') }}
ORDER BY date
