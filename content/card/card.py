import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.clickhouse_client import run_query
from queries.card.queries import ACTIVE_ADDRESSES, TOTAL_TXN, VOLUME
from charts.card.charts import create_transactions_chart, create_vol_chart, create_mau_chart

st.set_page_config(page_title="ALGORAND RWA - Pera Wallet Card", layout="wide")

def format_large_number(num):
    """Format large numbers with K, M, B suffixes"""
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{num:.0f}"

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_data(query):
    """Fetch data with automatic 1-hour refresh"""
    with st.spinner("Retrieving fresh data..."):
        data = run_query(query)
    return data



def render():
    # Calculate metrics
    rows, cols = fetch_data(TOTAL_TXN)
    tx_df = pd.DataFrame(rows, columns=cols)
    tx = tx_df.iloc[-1]['monthly_transactions']
    tx_delta = tx/tx_df.iloc[-2]['monthly_transactions'] - 1

    # Calculate metrics
    rows, cols = fetch_data(VOLUME)
    vol_df = pd.DataFrame(rows, columns=cols)
    vol = vol_df.iloc[-1]['monthly_volume'].sum()
    vol_delta = vol/vol_df.iloc[-2]['monthly_volume'].sum() - 1

    # Calculate metrics
    rows, cols = fetch_data(ACTIVE_ADDRESSES)
    mau_df = pd.DataFrame(rows, columns=cols)
    mau = mau_df.iloc[-1]['monthly_active_addresses']
    mau_delta = mau/mau_df.iloc[-2]['monthly_active_addresses'] - 1

    # First row with 4 columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label=f"Monthly Transactions",
            value=f"{format_large_number(tx)}",
            delta=f"{tx_delta*100:.2f}%",
            border=True
        )

    with col2:
        st.metric(
            label="Monthly Transfer Volume",
            value=f"${format_large_number(vol)}",
            delta=f"{vol_delta*100:.2f}%",
            border=True
        )

    with col3:
        st.metric(
            label="Monthly Active Addresses",
            value=f"{format_large_number(mau)}",
            delta=f"{mau_delta*100:.2f}%",
            border=True
        )

    st.divider()
    chart_options = {
        "monthly_transactions": "Monthly Transactions",
        "volume": "Transfer Volume",
        "mau": "Active Addresses"
    }

    selection = st.pills(
        "Chart Type",
        options=chart_options.keys(),
        format_func=lambda option: chart_options[option],
        selection_mode="single",
        default="monthly_transactions",
        label_visibility="collapsed",
        key="pills_card"  # Add this
    )

    # Add description based on selection
    chart_descriptions = {
        "monthly_transactions": "The sum of monthly transactions by Pera Wallet Card.",
        "volume": "The sum of monthly transferred volumes by Pera Wallet Card.",
        "mau": "Monthly number of wallets that have sent an on-chain transaction by using Pera Wallet Card."
    }

    if selection:
        st.info(chart_descriptions[selection])
    
    # Main content area
    try:
        # Fetch and prepare data
        with st.spinner("Loading data..."):
            # Market Cap Data
            tx_df['month'] = pd.to_datetime(tx_df['month'])
            tx_df = tx_df[tx_df['month'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

            # Volume Data
            vol_df['month'] = pd.to_datetime(vol_df['month'])
            vol_df = vol_df[vol_df['month'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

            # Active Wallets Data
            mau_df['month'] = pd.to_datetime(mau_df['month'])
            mau_df = mau_df[mau_df['month'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]
        
        # Display selected chart
        if selection == "monthly_transactions":
            fig = create_transactions_chart(tx_df)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(tx_df)
        
        elif selection == "volume":
            fig = create_vol_chart(vol_df)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(vol_df)
        
        elif selection == "mau":
            fig = create_mau_chart(mau_df)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(mau_df)
        
        else:
            st.info("👆 Please select a chart type above to view the data.")

    except NameError:
        # If fetch_data is not defined, show a placeholder
        st.error("⚠️ Data fetching function not found. Please ensure `fetch_data` is imported.")
        st.info("This dashboard requires the following constants to be defined: `MARKET_CAP`, `VOLUME`, `ACTIVE_WALLETS`")
        

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your data sources and try again.")