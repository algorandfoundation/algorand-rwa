import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

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
                    if col not in ['date', 'Date']]
    
    fig = go.Figure()
    
    # Add area trace for each stablecoin

    fig.add_trace(go.Scatter(
        x=mcap_df.index if 'date' not in mcap_df.columns.str.lower() else mcap_df[mcap_df.columns[mcap_df.columns.str.lower() == 'date'][0]],
        y=mcap_df['market_cap'],
        name='market_cap',
        mode='lines',
        stackgroup='one',
        fillcolor="#2d2df1",
        line=dict(width=0.5, color="#2d2df1"),
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Real Estate Market Cap',
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


def create_properties_chart(properties_df: pd.DataFrame) -> go.Figure:
    """
    Create a stacked bar chart for volume data.
    
    Args:
        vol_df: DataFrame with volume data
    
    Returns:
        Plotly Figure object with stacked bar chart
    """
    # Identify date column
    date_col = 'month_date'
 
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=properties_df[date_col] if date_col else properties_df.index,
        y=properties_df['monthly_tokenized'],
        name='Monthly Tokenized Properties',
        marker_color='#2d2df1',
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=properties_df[date_col] if date_col else properties_df.index,
        y=properties_df['cumulative_tokenized'],
        yaxis="y2",
        name='Total Tokenized Properties',
        mode='lines',
        line=dict(color='#17cac6'),
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title='Monthly Tokenized Properties',
        xaxis_title='Month',
        yaxis=dict(
            title='Tokenized Properties',
            tickformat=',.0f'
        ),
        yaxis2=dict(
            title='Total Tokenized Properties',
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

    fig.add_trace(go.Bar(
        x=mau_df[date_col] if date_col else mau_df.index,
        y=mau_df['monthly_unique_users'],
        name='Monthly Addresses',
        marker_color='#2d2df1',
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=mau_df[date_col] if date_col else mau_df.index,
        y=mau_df['cumulative_unique_users'],
        yaxis="y2",
        name='Total Unique Addresses',
        mode='lines',
        line=dict(color='#17cac6'),
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title='Monthly Active Users (Wallets)',
        xaxis_title='Month',
        yaxis=dict(
            title='Active Wallets',
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

