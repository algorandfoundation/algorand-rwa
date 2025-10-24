import yfinance as yf
import pandas as pd

def add_usd_volume(df, hafn_vol_col='hafn_vol', date_col='date'):
    """
    Fetch AFNUSD price from yfinance and calculate USD volume.
    
    Parameters:
    - df: DataFrame with date and hafn volume columns
    - hafn_vol_col: name of the HAFN volume column
    - date_col: name of the date column
    
    Returns:
    - DataFrame with added afnusd_close and hafn_vol_usd columns
    """
    # Ensure date column is datetime
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Fetch AFNUSD data
    afnusd = yf.download('AFNUSD=X', start=df[date_col].min(), end=df[date_col].max(), progress=False)
    # Handle multi-level columns from yfinance
    if isinstance(afnusd.columns, pd.MultiIndex):
        afnusd.columns = afnusd.columns.get_level_values(0)
    
    # Create a DataFrame with just the close prices
    price_df = pd.DataFrame({
        'date': afnusd.index,
        'afnusd_close': afnusd['Close'].values
    })
    
    price_df['date'] = pd.to_datetime(price_df['date']).dt.date
    df[date_col] = pd.to_datetime(df[date_col]).dt.date
    # Merge with original dataframe
    df = df.merge(price_df, on=date_col, how='left')
    
    # Forward fill NaN values (weekends/holidays)
    df['afnusd_close'] = df['afnusd_close'].ffill()
    
    # Calculate USD volume
    df['hafn_vol_usd'] = df['afnusd_close'] * df[hafn_vol_col]
    
    return df