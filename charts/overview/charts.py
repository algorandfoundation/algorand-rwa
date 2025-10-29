import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


def create_transactions_chart(tx_df: pd.DataFrame) -> go.Figure:
    """
    Create a stacked bar chart for volume data.
    
    Args:
        vol_df: DataFrame with volume data
    
    Returns:
        Plotly Figure object with stacked bar chart
    """
    # Identify date column
    date_col = None
    for col in tx_df.columns:
        if col.lower() in ['date', 'month', 'mt', 'time', 'timestamp']:
            date_col = col
            break
    
    # Get columns to plot (exclude date column and total columns)

    fig = go.Figure()
    
    # Add bar trace for each asset volume

    fig.add_trace(go.Bar(
        x=tx_df[date_col] if date_col else tx_df.index,
        y=tx_df['transactions'],
        name='Monthly Transactions',
        marker_color="#2d2df1",
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=tx_df[date_col] if date_col else tx_df.index,
        y=tx_df['total_transactions'],
        yaxis="y2",
        name='Total Transactions',
        mode='lines',
        line=dict(color='#17cac6'),
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Monthly Transactions Generated',
        xaxis_title='Date',
        yaxis=dict(
            title='Number Transactions',
            tickformat=',.0f'
        ),
        yaxis2=dict(
            title='Total Transactions',
            tickformat=',.0f',
            overlaying='y',
            side='right'
        ),
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
        if col.lower() in ['date', 'month', 'mt', 'time', 'timestamp']:
            date_col = col
            break
    
    # Get columns to plot (exclude date column)
    cols_to_plot = [col for col in mau_df.columns if col != date_col]
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=mau_df[date_col] if date_col else mau_df.index,
        y=mau_df['unique_wallets'],
        name='Monthly Unique Addresses',
        marker_color="#2d2df1",
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=mau_df[date_col] if date_col else mau_df.index,
        y=mau_df['cumulative_unique_wallets'],
        yaxis="y2",
        name='Total Unique Addresses',
        mode='lines',
        line=dict(color='#ffffff'),
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title='Monthly Active Addresses (Wallets)',
        xaxis_title='Month',
        yaxis=dict(
            title='Active Addresses',
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
        if col.lower() in ['date', 'month', 'mt', 'time', 'timestamp']:
            date_col = col
            break
    
    # Get columns to plot (exclude date column and total columns)

    fig = go.Figure()
    
    # Add bar trace for each asset volume

    fig.add_trace(go.Bar(
        x=vol_df[date_col] if date_col else vol_df.index,
        y=vol_df['volume'],
        name='Monthly USDC Volume',
        marker_color="#2d2df1",
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=vol_df[date_col] if date_col else vol_df.index,
        y=vol_df['cumulative_volume'],
        yaxis="y2",
        name='Total USDC Volume',
        mode='lines',
        line=dict(color='#17cac6'),
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Monthly USDC Volume',
        xaxis_title='Date',
        yaxis=dict(
            title='Volume ($)',
            tickformat=',.0f'
        ),
        yaxis2=dict(
            title='Total Volume ($)',
            tickformat=',.0f',
            overlaying='y',
            side='right'
        ),
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
        height=500
    )
    
    return fig