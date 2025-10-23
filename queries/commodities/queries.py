HOLDERS = """
SELECT COUNT(distinct addr_id) as holders
FROM mainnet.account_asset 
WHERE asset_id in (246516580, 246519683, 1241944285)
      and circulating 
      and amount > 0
"""

MARKET_CAP = """
SELECT
  *
FROM c_algorand.commodities_supply
"""

VOLUME = """
SELECT
  *
FROM c_algorand.commodities_volume
"""


ACTIVE_WALLETS = """
SELECT
  *
FROM c_algorand.commodities_active_wallets
"""