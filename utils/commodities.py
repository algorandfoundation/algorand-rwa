import pandas as pd
import numpy as np
import yfinance as yf
import requests
from datetime import datetime, timedelta, timezone
import warnings

def date_to_unix_timestamp(start_date_str, end_date_str):
  """
  Converts start and end dates in YYYY-MM-DD format to Unix timestamps.

  Args:
    start_date_str: Start date string in YYYY-MM-DD format.
    end_date_str: End date string in YYYY-MM-DD format.

  Returns:
    A tuple containing the start and end Unix timestamps.
  """

  start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
  end_date = datetime.strptime(end_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc) + timedelta(days=1) - timedelta(seconds=1) 

  start_timestamp = int(start_date.timestamp())
  end_timestamp = int(end_date.timestamp())

  return start_timestamp, end_timestamp

def get_close_price(start_date, end_date, asset_id):
    """
    Fetches an asset historical data from the API for the given interval.
    
    Args:
        start_timestamp: start unix timestamp
        end_timestamp: end unix timestamp

    Returns:
        pd.DataFrame: Dataframe containing the fetched data in daily intervals.
    """
    start_unix, end_unix = date_to_unix_timestamp(start_date, end_date)

    price_feed = f'https://indexer.vestige.fi/assets/{asset_id}/candles?network_id=0&interval=86400&start={start_unix}&end={end_unix}&denominating_asset_id=0&volume_in_denominating_asset=false'

    response = requests.get(price_feed)
    data = response.json()
    df = pd.DataFrame(data)
    return df

def combined_mcap_df(mcap_df):
    """
    Calculates the total market cap in USD by fetching price data for each asset
    and multiplying by their circulating supply.
    
    Args:
        mcap_df: DataFrame with date column and supply columns for each asset
                 (format: 'supply_{asset_id}_{asset_name}')
    
    Returns:
        pd.DataFrame: DataFrame with date and total_mcap_usd columns
    """
    start_date = str(mcap_df['date'].iloc[0])
    end_date = str(mcap_df['date'].iloc[-1])
    
    # Extract asset IDs and names from column names
    asset_info = []
    for col in mcap_df.columns:
        if col not in ['date', 'Date']:
            parts = col.split('_')
            if len(parts) >= 3 and parts[0] == 'supply':
                asset_id = parts[1]
                asset_name = parts[2].lower()
                asset_info.append({'id': asset_id, 'name': asset_name, 'col': col})
    
    # Create a copy of the dataframe with date
    result_df = mcap_df[['date']].copy()
    result_df['date'] = pd.to_datetime(result_df['date'])
    
    # Initialize total mcap column
    result_df['total_mcap_usd'] = 0.0
    
    # Fetch price data for each asset and calculate mcap
    for asset in asset_info:
        try:
            # Get price data
            price_df = get_close_price(start_date, end_date, asset['id'])
            
            # Convert timestamp to date
            price_df['date'] = pd.to_datetime(price_df['timestamp'], unit='s').dt.date
            price_df['date'] = pd.to_datetime(price_df['date'])
            
            # Merge with mcap data
            merged = result_df.merge(
                price_df[['date', 'close']], 
                on='date', 
                how='left'
            )
            
            # Forward fill missing prices
            merged['close'] = merged['close'].ffill()
            
            # Calculate mcap for this asset (supply * price)
            asset_mcap = mcap_df[asset['col']].fillna(0).values * merged['close'].fillna(0).values
            
            # Add to total mcap
            result_df['total_mcap_usd'] += asset_mcap
            
            # Optionally store individual asset mcap
            result_df[f"{asset['name']}_mcap_usd"] = asset_mcap
            
        except Exception as e:
            print(f"Error processing asset {asset['name']} (ID: {asset['id']}): {e}")
            continue
    
    return result_df

def combined_volume_df(vol_df):
    """
    Calculates the total market cap in USD by fetching price data for each asset
    and multiplying by their circulating supply.
    
    Args:
        mcap_df: DataFrame with date column and supply columns for each asset
                 (format: 'supply_{asset_id}_{asset_name}')
    
    Returns:
        pd.DataFrame: DataFrame with date and total_mcap_usd columns
    """
    start_date = str(vol_df['date'].iloc[0])
    end_date = str(vol_df['date'].iloc[-1])
    
    # Extract asset IDs and names from column names
    asset_info = []
    for col in vol_df.columns:
        if col not in ['date', 'Date']:
            parts = col.split('_')
            if len(parts) >= 3 and parts[0] == 'volume':
                asset_id = parts[1]
                asset_name = parts[2].lower()
                asset_info.append({'id': asset_id, 'name': asset_name, 'col': col})
    
    # Create a copy of the dataframe with date
    result_df = vol_df[['date']].copy()
    result_df['date'] = pd.to_datetime(result_df['date'])
    
    # Initialize total mcap column
    result_df['total_vol_usd'] = 0.0
    
    # Fetch price data for each asset and calculate mcap
    for asset in asset_info:
        try:
            # Get price data
            price_df = get_close_price(start_date, end_date, asset['id'])
            
            # Convert timestamp to date
            price_df['date'] = pd.to_datetime(price_df['timestamp'], unit='s').dt.date
            price_df['date'] = pd.to_datetime(price_df['date'])
            
            # Merge with mcap data
            merged = result_df.merge(
                price_df[['date', 'close']], 
                on='date', 
                how='left'
            )
            
            # Forward fill missing prices
            merged['close'] = merged['close'].ffill()
            
            # Calculate mcap for this asset (supply * price)
            asset_vol = vol_df[asset['col']].fillna(0).values * merged['close'].fillna(0).values
            
            # Add to total mcap
            result_df['total_vol_usd'] += asset_vol
            
            # Optionally store individual asset mcap
            result_df[f"{asset['name']}_vol_usd"] = asset_vol
            
        except Exception as e:
            print(f"Error processing asset {asset['name']} (ID: {asset['id']}): {e}")
            continue
    
    return result_df