import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


# Asset name mapping
ASSET_NAME_MAP = {
    'gold$': 'GOLD$',
    'silver$': 'SILVER$',
    'gold': 'Gold'
}

# Color mapping for assets
ASSET_COLOR_MAP = {
    'GOLD$': '#2D2DF1',
    'SILVER$': '#17CAC6',
    'Gold': '#FFFFFF'
}


def format_column_name(col: str) -> str:
    """
    Format column name by extracting the asset name and applying proper casing.
    
    Args:
        col: Column name in format like 'supply_assetid_asset'
    
    Returns:
        Formatted asset name
    """
    # Extract the last part after the last underscore
    parts = col.split('_')
    asset = parts[0].lower()
    
    # Apply mapping or return as-is if not in map
    return ASSET_NAME_MAP.get(asset, asset.upper())


def create_mcap_chart(mcap_df: pd.DataFrame) -> go.Figure:
    """
    Create an area chart for market cap data.
    
    Args:
        mcap_df: DataFrame with market cap data. Should contain a date column
                 and multiple stablecoin columns. 'total_circulating_supply' 
                 column will be excluded.
    
    Returns:
        Plotly Figure object with area chart
    """
    # Get all columns except total_circulating_supply
    cols_to_plot = [col for col in mcap_df.columns 
                    if col not in ['total_mcap_usd', 'date', 'Date']]
    
    fig = go.Figure()
    
    # Add area trace for each stablecoin
    for col in cols_to_plot:
        asset_name = format_column_name(col)
        fig.add_trace(go.Scatter(
            x=mcap_df.index if 'date' not in mcap_df.columns.str.lower() else mcap_df[mcap_df.columns[mcap_df.columns.str.lower() == 'date'][0]],
            y=mcap_df[col],
            name=asset_name,
            mode='lines',
            stackgroup='one',
            fillcolor=ASSET_COLOR_MAP.get(asset_name),
            line=dict(width=0.5, color=ASSET_COLOR_MAP.get(asset_name)),
            hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Stablecoin Market Cap',
        xaxis_title='Date',
        yaxis_title='Market Cap (USD)',
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(tickformat=',.0f'),
        height=500
    )
    
    return fig


def create_volume_chart(vol_df: pd.DataFrame) -> go.Figure:
    """
    Create a stacked bar chart for volume data.
    
    Args:
        vol_df: DataFrame with volume data
    
    Returns:
        Plotly Figure object with stacked bar chart
    """
    # Identify date column
    date_col = None
    for col in vol_df.columns:
        if col.lower() in ['date', 'time', 'timestamp']:
            date_col = col
            break
    
    # Get columns to plot (exclude date column and total_stablecoin_volume)
    cols_to_plot = [col for col in vol_df.columns 
                    if col not in [date_col, 'total_vol_usd']]
    
    fig = go.Figure()
    
    # Add bar trace for each stablecoin
    for col in cols_to_plot:
        asset_name = format_column_name(col)
        fig.add_trace(go.Bar(
            x=vol_df[date_col] if date_col else vol_df.index,
            y=vol_df[col],
            name=asset_name,
            marker_color=ASSET_COLOR_MAP.get(asset_name),
            hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Stablecoin Trading Volume',
        xaxis_title='Date',
        yaxis_title='Volume (USD)',
        barmode='stack',
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        yaxis=dict(tickformat=',.0f'),
        height=500
    )
    
    return fig


def create_mau_chart(mau_df: pd.DataFrame) -> go.Figure:
    """
    Create a bar chart for monthly active users data.
    
    Args:
        mau_df: DataFrame with monthly active users data
    
    Returns:
        Plotly Figure object with bar chart
    """
    # Identify date column
    date_col = None
    for col in mau_df.columns:
        if col.lower() in ['date', 'month', 'time', 'timestamp']:
            date_col = col
            break
    
    # Get columns to plot (exclude date column)
    cols_to_plot = [col for col in mau_df.columns if col != date_col]
    
    fig = go.Figure()
    
    # Add bar trace for each stablecoin with uniform color
    for col in cols_to_plot:
        asset_name = format_column_name(col)
        fig.add_trace(go.Bar(
            x=mau_df[date_col] if date_col else mau_df.index,
            y=mau_df[col],
            name=asset_name,
            marker_color='#2d2df1',
            hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Monthly Active Users (Wallets)',
        xaxis_title='Month',
        yaxis_title='Active Wallets',
        barmode='group',
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(tickformat=',.0f'),
        height=500
    )
    
    return fig

