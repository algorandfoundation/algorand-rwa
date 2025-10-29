import streamlit as st
import pandas as pd
import subprocess
import time
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.clickhouse_client import run_query
from utils.real_estate import get_lofty_mcap
from queries.real_estate.queries import PROPERTIES, MARKET_CAP, ACTIVE_WALLETS, MARKET_VOLUME, AMM_BUY, AMM_SELL
from charts.real_estate.charts import create_mcap_chart, create_properties_chart, create_mau_chart, create_volumes_chart

st.set_page_config(page_title="ALGORAND RWA - Real Estate", layout="wide")

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

@st.cache_data(ttl=3600)  # Auto-refresh cache every hour
def fetch_data(query):
    """Fetch data with automatic 1-hour refresh"""
    return run_query(query)

@st.cache_data(ttl=3600*12)  # Auto-refresh cache every hour
def fetch_mcap():
    """Fetch data with automatic 12-hour refresh"""
    return get_lofty_mcap()


def render():
    # Calculate metrics
    rows, cols = fetch_data(PROPERTIES)
    property_df = pd.DataFrame(rows, columns=cols)
    properties = property_df.iloc[-1]['cumulative_tokenized']
    properties_delta = properties/property_df.iloc[-2]['cumulative_tokenized'] - 1

    mcap_df = fetch_mcap()
    mcap = mcap_df.iloc[-1]['market_cap']
    mcap_delta = mcap/mcap_df.iloc[-30]['market_cap'] - 1

    rows, cols = fetch_data(ACTIVE_WALLETS)
    mau_df = pd.DataFrame(rows, columns=cols)
    mau = mau_df.iloc[-1]['monthly_unique_users']
    mau_delta = mau/mau_df.iloc[-2]['monthly_unique_users'] - 1

    rows, cols = fetch_data(MARKET_VOLUME)
    vol_df = pd.DataFrame(rows, columns=cols)
    
    rows, cols = fetch_data(AMM_BUY)
    amm_buy_df = pd.DataFrame(rows, columns=cols)
    
    rows, cols = fetch_data(AMM_SELL)
    amm_sell_df = pd.DataFrame(rows, columns=cols)
    
    vol_df = vol_df.merge(amm_buy_df, on='month', how='left')
    vol_df = vol_df.merge(amm_sell_df, on='month', how='left')
    vol_df['month_vol'] = vol_df['market_volume'] + vol_df['monthly_buy_volume'] + vol_df['monthly_sell_volume']

    vol = vol_df.iloc[-1]['month_vol']
    vol_delta = vol/vol_df.iloc[-2]['month_vol'] - 1

    # First row with 4 columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label=f"Market Cap",
            value=f"${format_large_number(mcap)}",
            delta=f"{mcap_delta*100:.2f}%",
            border=True
        )

    with col2:
        st.metric(
            label=f"Monthly Volume",
            value=f"${format_large_number(vol)}",
            delta=f"{vol_delta*100:.2f}%",
            border=True
        )

    with col3:
        st.metric(
            label="Total Tokenized Properties",
            value=f'{format_large_number(properties)}',
            delta=f"{properties_delta*100:.2f}%",
            border=True
        )

    with col4:
        st.metric(
            label="Monthly Active Addresses",
            value=f"{format_large_number(mau)}",
            delta=f"{mau_delta*100:.2f}%",
            border=True
        )

        
    st.divider()
    chart_options = {
        "market_cap": "Market Cap",
        "monthly_volume_re": "Monthly Volume",
        "monthly_properties": "Tokenized Properties",
        "mau": "Active Addresses"
    }

    selection = st.pills(
        "Chart Type",
        options=chart_options.keys(),
        format_func=lambda option: chart_options[option],
        selection_mode="single",
        default="market_cap",
        label_visibility="collapsed",
        key="pills_realestate"  # Add this
    )

    # Add description based on selection
    chart_descriptions = {
        "market_cap": "The evolution of the value of all tokenized properties on Algorand.",
        "monthly_volume_re": "Monthly volume transacted on Lofty.",
        "monthly_properties": "The sum of monthly tokenized properties.",
        "mau": "Monthly number of wallets that have sent an on-chain transaction."
    }

    if selection:
        st.info(chart_descriptions[selection])
    
    # Main content area
    try:
        # Fetch and prepare data
        with st.spinner("Loading data..."):
            # Market Cap Data
            mcap_df['date'] = pd.to_datetime(mcap_df['date'])
            mcap_df = mcap_df[mcap_df['date'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]
            
            vol_df['month'] = pd.to_datetime(vol_df['month'])
            vol_df = vol_df[vol_df['month'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

        # Display selected chart
        if selection == "market_cap":
            fig = create_mcap_chart(mcap_df)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(mcap_df)

        elif selection == "monthly_volume_re":
            fig = create_volumes_chart(vol_df)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(vol_df)

        elif selection == "monthly_properties":
            fig = create_properties_chart(property_df)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(mau_df)
        
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