import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


# Color mapping for assets
ASSET_COLOR_MAP = {
    'MannDeshi': '#2D2DF1',
    'LabTrace': '#17CAC6'
}

def create_certificates_chart(cert_df: pd.DataFrame) -> go.Figure:
    """
    Create a stacked bar chart for volume data.
    
    Args:
        vol_df: DataFrame with volume data
    
    Returns:
        Plotly Figure object with stacked bar chart
    """
    # Identify date column
    date_col = None
    for col in cert_df.columns:
        if col.lower() in ['date', 'time', 'timestamp']:
            date_col = col
            break
    
    # Get columns to plot (exclude date column and total columns)
    cols_to_plot = ['MannDeshi', 'LabTrace']
    
    fig = go.Figure()
    
    # Add bar trace for each asset volume
    for col in cols_to_plot:
        fig.add_trace(go.Bar(
            x=cert_df[date_col] if date_col else cert_df.index,
            y=cert_df[col],
            name=col,
            marker_color=ASSET_COLOR_MAP.get(col),
            hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
        ))
    
    fig.add_trace(go.Scatter(
        x=cert_df[date_col] if date_col else cert_df.index,
        y=cert_df['cumulative_certificates'],
        yaxis="y2",
        name='Certificates Issued',
        mode='lines',
        line=dict(color='#ffffff'),
        hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Monthly Certificates Issued',
        xaxis_title='Date',
        yaxis=dict(
            title='Number of Certificates Issued',
            tickformat=',.0f'
        ),
        yaxis2=dict(
            title='Total Certificates Issued',
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
        if col.lower() in ['date', 'month', 'time', 'timestamp']:
            date_col = col
            break
    
    # Get columns to plot (exclude date column)
    cols_to_plot = [col for col in mau_df.columns if col != date_col]
    
    fig = go.Figure()
    
    # Add bar trace for each stablecoin with uniform color

    # Get columns to plot (exclude date column and total columns)
    cols_to_plot = ['MannDeshi', 'LabTrace']
    
    fig = go.Figure()
    
    # Add bar trace for each asset volume
    for col in cols_to_plot:
        fig.add_trace(go.Bar(
            x=mau_df[date_col] if date_col else mau_df.index,
            y=mau_df[col],
            name=col,
            marker_color=ASSET_COLOR_MAP.get(col),
            hovertemplate='<b>%{fullData.name}</b>: %{y:,.0f}<extra></extra>'
        ))
    
    fig.add_trace(go.Scatter(
        x=mau_df[date_col] if date_col else mau_df.index,
        y=mau_df['cumulative_users'],
        yaxis="y2",
        name='Total Unique Addresses',
        mode='lines',
        line=dict(color='#ffffff'),
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

