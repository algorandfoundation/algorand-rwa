import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.clickhouse_client import run_query
from utils.commodities import combined_mcap_df, combined_volume_df
from queries.commodities.queries import HOLDERS, MARKET_CAP, VOLUME, ACTIVE_WALLETS
from charts.commodities.charts import create_mcap_chart, create_volume_chart, create_mau_chart

st.set_page_config(page_title="ALGORAND RWA - Stablecoins", layout="wide")

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


def render():
    # Calculate metrics
    rows, cols = fetch_data(MARKET_CAP)
    mcap_df = pd.DataFrame(rows, columns=cols)
    mcap_df = combined_mcap_df(mcap_df)
    mcap = mcap_df.iloc[-1]['total_mcap_usd']
    mcap_delta = mcap/mcap_df.iloc[-2]['total_mcap_usd'] - 1

    holders, _ = fetch_data(HOLDERS)

    holders = holders[0][0]

    # Calculate metrics
    rows, cols = fetch_data(VOLUME)
    vol_df = pd.DataFrame(rows, columns=cols)
    vol_df = combined_volume_df(vol_df)
    last30d_vol = vol_df[-30:]['total_vol_usd'].sum()
    vol_delta = last30d_vol/vol_df[-60:-30]['total_vol_usd'].sum() - 1

    # Calculate metrics
    rows, cols = fetch_data(ACTIVE_WALLETS)
    mau_df = pd.DataFrame(rows, columns=cols)
    mau = mau_df.iloc[-1]['active_wallets']
    mau_delta = mau/mau_df.iloc[-2]['active_wallets'] - 1

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
            label="Monthly Transfer Volume",
            value=f"${format_large_number(last30d_vol)}",
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

    with col4:
        st.metric(
            label="Holders",
            value=f"{format_large_number(holders)}",
            delta="_",
            delta_color="off",
            border=True
        )
    st.divider()
    chart_options = {
        "market_cap_commodities": "Commodities Market Cap",
        "volume_commodities": "Commodities Transfer Volume",
        "mau_commodities": "Commodities Active Addresses"
    }

    selection = st.pills(
        "Chart Type",
        options=chart_options.keys(),
        format_func=lambda option: chart_options[option],
        selection_mode="single",
        default="market_cap_commodities",
        label_visibility="collapsed"
    )

    # Add description based on selection
    chart_descriptions = {
        "market_cap_commodities": "The Market Cap by commodities on Algorand.",
        "volume_commodities": "The sum of monthly transferred volumes by commodity.",
        "mau_commodities": "Monthly number of wallets that have sent an on-chain transaction."
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

            # Volume Data
            vol_df['date'] = pd.to_datetime(vol_df['date'])
            vol_df = vol_df[vol_df['date'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

            # Group by month and sum all other columns
            monthly_vol = (
                vol_df
                .groupby(vol_df['date'].dt.to_period('M'))
                .sum(numeric_only=True)
                .reset_index()
            )

            # 🔧 Convert 'date' column from Period to Timestamp (fixes JSON serialization error)
            monthly_vol['date'] = monthly_vol['date'].dt.to_timestamp()

            # Active Wallets Data
            mau_df['month'] = pd.to_datetime(mau_df['month'])
            mau_df = mau_df[mau_df['month'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

        # Display selected chart
        if selection == "market_cap_commodities":
            fig = create_mcap_chart(mcap_df)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(mcap_df)
        
        elif selection == "volume_commodities":
            fig = create_volume_chart(monthly_vol)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(vol_df)
        
        elif selection == "mau_commodities":
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