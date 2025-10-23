{{ config(materialized='view') }}

-- models/staging/stg_mint_burn_wallets.sql

SELECT arrayJoin([
  334314076, 337849393, 337846447, 345003642, 345005068, -- USDC
  138399456, -- USDT
  1445874475, 1332138752, 3042324867, -- GOUSD
  1355935955, 2741347927, 2853884730, 4015457176 -- XUSD
]) AS wallet_id
