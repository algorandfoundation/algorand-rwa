import pandas as pd 
import requests
import time

def get_tvl_data(coin_id):
    """
    This function fetches TVL data from Defillama and returns it as a DataFrame.
    
    Args:
        coin_id: the name of the crypto we are getting the data
    
    Returns:
        pd.DataFrame: Melted dataframe with Protocol, date (variable), and value columns
    """
    # Construct the URL
    full_url_all = f'https://api.llama.fi/simpleChainDataset/{coin_id}?pool2=true&staking=true&borrowed=true&doublecounted=true&liquidstaking=true&vesting=true&govtokens=true'
    full_url_borrows = f'https://api.llama.fi/simpleChainDataset/{coin_id}?pool2=true&staking=true&borrowed=false&doublecounted=true&liquidstaking=true&vesting=true&govtokens=true'

    # Download the CSV
    response = requests.get(full_url_all, headers={'User-agent': 'Price Scrapper'})
    response2 = requests.get(full_url_borrows, headers={'User-agent': 'Price Scrapper'})
    
    if response.status_code == 429:
        time.sleep(int(response.headers["Retry-After"]))
        # Retry the request
        response = requests.get(full_url_all, headers={'User-agent': 'Price Scrapper'})
        response2 = requests.get(full_url_borrows, headers={'User-agent': 'Price Scrapper'})
    
    if response.status_code == 200:
        # Read CSV directly from response content into DataFrame
        from io import StringIO
        tvl = pd.read_csv(StringIO(response.content.decode('utf-8')))
        tvl2 = pd.read_csv(StringIO(response2.content.decode('utf-8')))
        
        # Melt the dataframe
        tvl = tvl.melt(id_vars='Protocol')
        tvl = tvl[tvl['Protocol']=='Folks Finance Lending'].reset_index(drop=True)

        tvl2 = tvl2.melt(id_vars='Protocol')
        tvl2 = tvl2[tvl2['Protocol']=='Folks Finance Lending'].reset_index(drop=True)
        

        # Convert date column
        tvl['variable'] = pd.to_datetime(tvl['variable'], format="%d/%m/%Y")
        tvl2['variable'] = pd.to_datetime(tvl2['variable'], format="%d/%m/%Y")
        

        # Optionally rename columns for clarity
        tvl = tvl.rename(columns={'variable': 'date', 'value': 'tvl'})
        tvl2 = tvl2.rename(columns={'variable': 'date', 'value': 'no_borrows'})
        
        tvl = tvl.merge(tvl2[['date','no_borrows']], on='date', how='left')
        tvl['borrows'] = tvl['tvl'] - tvl['no_borrows']
        return tvl
    else:
        print(f"Failed to download CSV for {coin_id}. Status code: {response.status_code}")
        return None