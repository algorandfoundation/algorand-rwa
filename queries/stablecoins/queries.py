HOLDERS = """
SELECT COUNT(distinct addr_id) as holders
FROM mainnet.account_asset 
WHERE asset_id in (31566704, 312769, 760037151, 672913181)
      and circulating 
      and amount > 0
"""

MARKET_CAP = """
SELECT
  *
FROM c_algorand.stablecoin_supply
"""

VOLUME = """
SELECT
  *
FROM c_algorand.stablecoin_volume
"""


ACTIVE_WALLETS = """
SELECT
  *
FROM c_algorand.stablecoin_active_wallets
"""