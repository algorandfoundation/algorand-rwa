import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


# Asset name mapping
ASSET_NAME_MAP = {
    'algo': 'ALGO',
    'stable': 'Stablecoins',
    'hafn': 'HAFN'
}

# Color mapping for assets
ASSET_COLOR_MAP = {
    'ALGO': '#2D2DF1',
    'Stablecoins': '#17CAC6',
    'HAFN': '#FFFFFF'
}


def format_column_name(col: str) -> str:
    """
    Format column name by extracting the asset name and applying proper casing.
    
    Args:
        col: Column name in format like 'algo_transactions'
    
    Returns:
        Formatted asset name
    """
    # Extract the first part before the first underscore
    parts = col.split('_')
    asset = parts[0].lower()
    
    # Apply mapping or return as-is if not in map
    return ASSET_NAME_MAP.get(asset, asset.upper())


def create_payments_chart(payments_df: pd.DataFrame) -> go.Figure:
    """
    Create a stacked bar chart for payment transactions.
    
    Args:
        payments_df: DataFrame with payment data. Should contain a date column
                     and transaction columns like 'algo_transactions', 'stable_transactions', etc.
    
    Returns:
        Plotly Figure object with stacked bar chart
    """
    # Identify date column
    date_col = None
    for col in payments_df.columns:
        if col.lower() in ['date', 'time', 'timestamp']:
            date_col = col
            break
    
    # Get columns to plot (exclude date and total columns)
    cols_to_plot = [col for col in payments_df.columns 
                    if col not in [date_col, 'total_transactions'] and 'transaction' in col.lower()]
    
    fig = go.Figure()
    
    # Add bar trace for each transaction type
    for col in cols_to_plot:
        asset_name = format_column_name(col)
        fig.add_trace(go.Bar(
            x=payments_df[date_col] if date_col else payments_df.index,
            y=payments_df[col],
            name=asset_name,
            marker_color=ASSET_COLOR_MAP.get(asset_name),
            hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Payment Transactions',
        xaxis_title='Date',
        yaxis_title='Number of Transactions',
        barmode='stack',
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
    
    # Get columns to plot (exclude date column and total columns)
    cols_to_plot = [col for col in vol_df.columns 
                    if col not in [date_col] and 'total' not in col.lower() and 'vol' in col.lower()]
    
    fig = go.Figure()
    
    # Add bar trace for each asset volume
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
        title='Trading Volume',
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


def create_addresses_chart(addresses_df: pd.DataFrame) -> go.Figure:
    """
    Create a grouped bar chart for unique addresses with a line showing total unique addresses.
    
    Args:
        addresses_df: DataFrame with unique addresses data. Should include columns like
                      'algo_addresses', 'stable_addresses', 'hafn_addresses', and 'total_unique_addresses'
    
    Returns:
        Plotly Figure object with grouped bars and line chart
    """
    # Identify date column
    date_col = None
    for col in addresses_df.columns:
        if col.lower() in ['date', 'month', 'time', 'timestamp']:
            date_col = col
            break
    
    # Get columns to plot (exclude date and total columns)
    cols_to_plot = [col for col in addresses_df.columns 
                    if col not in [date_col, 'total_unique_addresses'] and 'address' in col.lower()]
    
    fig = go.Figure()
    
    # Add bar trace for each asset's addresses (grouped, not stacked)
    for col in cols_to_plot:
        asset_name = format_column_name(col)
        fig.add_trace(go.Bar(
            x=addresses_df[date_col] if date_col else addresses_df.index,
            y=addresses_df[col],
            name=asset_name,
            marker_color=ASSET_COLOR_MAP.get(asset_name),
            hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
        ))
    
    # Add line trace for total unique addresses on secondary y-axis
    if 'total_unique_addresses' in addresses_df.columns:
        fig.add_trace(go.Scatter(
            x=addresses_df[date_col] if date_col else addresses_df.index,
            y=addresses_df['total_unique_addresses'],
            yaxis="y2",
            name='Total Unique Addresses',
            mode='lines',
            line=dict(color='#bfbff9', width=2),
            hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Unique Active Addresses',
        xaxis_title='Date',
        yaxis=dict(
            title='Addresses by Asset',
            tickformat=',.0f'
        ),
        yaxis2=dict(
            title='Total Unique Addresses',
            tickformat=',.0f',
            overlaying='y',
            side='right'
        ),
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
        height=500
    )
    
    return fig