import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

def create_dep_chart(borrows_df: pd.DataFrame) -> go.Figure:
    """
    Create an area chart for market cap data.
    
    Args:
        borrows_df: DataFrame with market cap data. Should contain a date column
                 and multiple stablecoin columns. 'total_circulating_supply' 
                 column will be excluded.
    
    Returns:
        Plotly Figure object with area chart
    """

    fig = go.Figure()
    
    # Add area trace for each stablecoin

    fig.add_trace(go.Scatter(
        x=borrows_df.index if 'date' not in borrows_df.columns.str.lower() else borrows_df[borrows_df.columns[borrows_df.columns.str.lower() == 'date'][0]],
        y=borrows_df['tvl'],
        name='Deposits',
        mode='lines',
        stackgroup='one',
        fillcolor="#2d2df1",
        line=dict(width=0.5, color="#2d2df1"),
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Private Credit Deposits',
        xaxis_title='Date',
        yaxis_title='Deposited Amount (USD)',
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


def create_borrows_chart(borrows_df: pd.DataFrame) -> go.Figure:
    """
    Create an area chart for market cap data.
    
    Args:
        borrows_df: DataFrame with market cap data. Should contain a date column
                 and multiple stablecoin columns. 'total_circulating_supply' 
                 column will be excluded.
    
    Returns:
        Plotly Figure object with area chart
    """
    # Get all columns except total_circulating_supply
    cols_to_plot = [col for col in borrows_df.columns 
                    if col not in ['date', 'Date']]
    
    fig = go.Figure()
    
    # Add area trace for each stablecoin

    fig.add_trace(go.Scatter(
        x=borrows_df.index if 'date' not in borrows_df.columns.str.lower() else borrows_df[borrows_df.columns[borrows_df.columns.str.lower() == 'date'][0]],
        y=borrows_df['borrows'],
        name='Borrows',
        mode='lines',
        stackgroup='one',
        fillcolor="#2d2df1",
        line=dict(width=0.5, color="#2d2df1"),
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Private Credit Borrows',
        xaxis_title='Date',
        yaxis_title='Borrowed Amount (USD)',
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

