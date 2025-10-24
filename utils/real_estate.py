import pandas as pd 
import requests
import time

def get_lofty_mcap():
    """
    This function fetches TVL data from Defillama and returns it as a DataFrame.
    
    Args:
        coin_id: the name of the crypto we are getting the data
    
    Returns:
        pd.DataFrame: Melted dataframe with Protocol, date (variable), and value columns
    """
    # Construct the URL
    full_url_all = f'https://api.llama.fi/protocol/lofty'

    # Download the CSV
    response = requests.get(full_url_all, headers={'User-agent': 'Price Scrapper'})

    if response.status_code == 429:
        time.sleep(int(response.headers["Retry-After"]))
        # Retry the request
        response = requests.get(full_url_all, headers={'User-agent': 'Price Scrapper'})

    if response.status_code == 200:
        tvl = pd.DataFrame(response.json()['tvl'])

        # For each column except the date column
        for col in tvl.columns:
            if col != 'date':  # Skip the date column
                # Extract the peggedUSD value for each row in the column
                tvl[col] = tvl[col].apply(lambda x: x.get('totalLiquidityUSD') if isinstance(x, dict) else x)

        tvl = tvl.rename(columns={'totalLiquidityUSD': 'market_cap'})
        tvl['date'] = pd.to_datetime(tvl['date'], unit='s').dt.date
        return tvl[:-1]
    else:
        print(f"Failed to get Lofty Mcap. Status code: {response.status_code}")
        return None