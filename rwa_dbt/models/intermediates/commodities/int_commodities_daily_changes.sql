{{ config(materialized='table') }}

WITH combined AS (

  SELECT
    date,
    asset_id,
    asset,
    SUM(mints) AS daily_mints,
    0 AS daily_burns,
    SUM(mints) AS net_change
  FROM {{ ref('int_commodities_mints') }}
  GROUP BY date, asset_id, asset

  UNION ALL

  SELECT
    date,
    asset_id,
    asset,
    0 AS daily_mints,
    SUM(burns) AS daily_burns,
    -SUM(burns) AS net_change
  FROM {{ ref('int_commodities_burns') }}
  GROUP BY date, asset_id, asset
),

aggregated AS (
  SELECT
    date,
    asset_id,
    asset,
    SUM(daily_mints) AS daily_mints,
    SUM(daily_burns) AS daily_burns,
    SUM(net_change) AS net_change
  FROM combined
  GROUP BY date, asset_id, asset
)

SELECT
  date,
  asset_id,
  asset,
  daily_mints,
  daily_burns,
  net_change,
  SUM(net_change) OVER (
    PARTITION BY asset_id 
    ORDER BY date 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS circulating_supply
FROM aggregated
ORDER BY date, asset_id
