import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.clickhouse_client import run_query
from utils.hafn_volume import add_usd_volume
from queries.micropayments.queries import VOLUME_1, VOLUME_2, TRANSACTIONS, ACTIVE_WALLETS
from charts.micropayments.charts import create_payments_chart, create_volume_chart, create_addresses_chart

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

def render():
    # Calculate metrics
    rows, cols = fetch_data(VOLUME_1)
    vol_df = pd.DataFrame(rows, columns=cols)

    rows, cols = fetch_data(VOLUME_2)
    hafn_vol_df = pd.DataFrame(rows, columns=cols)
    hafn_vol = add_usd_volume(hafn_vol_df)
    
    vol_df = vol_df.merge(hafn_vol, on='date', how='left')
    vol_df['volume'] = vol_df['total_vol'] + vol_df['hafn_vol_usd']
    last30d_vol = vol_df[-30:]['volume'].sum()
    vol_delta = last30d_vol/vol_df[-60:-30]['volume'].sum() - 1

    rows, cols = fetch_data(TRANSACTIONS)
    tx_df = pd.DataFrame(rows, columns=cols)
    last30d_tx = tx_df[-30:]['total_transactions'].sum()
    tx_delta = last30d_tx/tx_df[-60:-30]['total_transactions'].sum() - 1

    rows, cols = fetch_data(ACTIVE_WALLETS)
    mau_df = pd.DataFrame(rows, columns=cols)
    mau = mau_df.iloc[-1]['total_unique_addresses']
    mau_delta = mau/mau_df.iloc[-2]['total_unique_addresses'] - 1


    # First row with 4 columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label=f"Monthly Payments",
            value=f'{format_large_number(last30d_tx)}',
            delta=f"{tx_delta*100:,.2f}%",
            border=True
        )

    with col2:
        st.metric(
            label="Monthly Volume",
            value=f"${format_large_number(last30d_vol)}",
            delta=f"{vol_delta*100:,.2f}%",
            border=True
        )

    with col3:
        st.metric(
            label="Monthly Active Addresses",
            value=f"{mau:,.0f}",
            delta=f"{mau_delta*100:.2f}%",
            border=True
        )

        
    st.divider()
    chart_options = {
        "payments": "Monthly Payments",
        "monthly_volume_micro": "Monthly Volume",
        "mau_micropayments": "Active Addresses"
    }

    selection = st.pills(
        "Chart Type",
        options=chart_options.keys(),
        format_func=lambda option: chart_options[option],
        selection_mode="single",
        default="payments",
        label_visibility="collapsed"
    )

    # Add description based on selection
    chart_descriptions = {
        "payments": "Market Cap shows the evolution of the value  of all tokenized properties on Algorand.",
        "monthly_volume_micro": "The sum of monthly tokenized properties.",
        "mau_micropayments": "Monthly number of unique wallets that have sent an on-chain transaction."
    }

    if selection:
        st.info(chart_descriptions[selection])
    
    # Main content area
    try:
        # Fetch and prepare data
        with st.spinner("Loading data..."):
            # Market Cap Data
            tx_df['date'] = pd.to_datetime(tx_df['date'])
            tx_df = tx_df[tx_df['date'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

            # Volume Data
            vol_df['date'] = pd.to_datetime(vol_df['date'])
            vol_df = vol_df[vol_df['date'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

            monthly_tx = (
                tx_df
                .groupby(tx_df['date'].dt.to_period('M'))
                .sum(numeric_only=True)
                .reset_index()
            )
            monthly_tx['date'] = monthly_tx['date'].dt.to_timestamp()

            # Group by month and sum all other columns
            monthly_vol = (
                vol_df[['date', 'algo_vol', 'stable_vol', 'hafn_vol_usd']]
                .groupby(vol_df['date'].dt.to_period('M'))
                .sum(numeric_only=True)
                .reset_index()
            )
            monthly_vol['date'] = monthly_vol['date'].dt.to_timestamp()

        # Display selected chart
        if selection == "payments":
            st.header("Monthly Payments")
            st.markdown("Stacked bar chart to dispplay the different micropayments on Algorand.")
            fig = create_payments_chart(monthly_tx)
            st.plotly_chart(fig, use_container_width=True)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(monthly_tx, width='stretch')
        
        elif selection == "monthly_volume_micro":
            st.header("Monthly Volume transferred")
            st.markdown("Stacked bar chart showing the monthly volume on micropayments.")
            fig = create_volume_chart(monthly_vol)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(mau_df, width='stretch')
        
        elif selection == "mau_micropayments":
            st.header("Active Addresses")
            st.markdown("Bar chart showing the number of active wallets on Lofty.")
            fig = create_addresses_chart(mau_df)
            st.plotly_chart(fig, use_container_width=True)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(mau_df, use_container_width=True)
        
        else:
            st.info("👆 Please select a chart type above to view the data.")

    except NameError:
        # If fetch_data is not defined, show a placeholder
        st.error("⚠️ Data fetching function not found. Please ensure `fetch_data` is imported.")
        st.info("This dashboard requires the following constants to be defined: `MARKET_CAP`, `VOLUME`, `ACTIVE_WALLETS`")
        
        # Show example of what the dashboard would look like
        st.markdown("---")
        st.subheader("Dashboard Preview")
        st.markdown("Once data is connected, you'll be able to:")
        st.markdown("- 📈 View market cap trends")
        st.markdown("- 📊 Compare trading volumes")
        st.markdown("- 👥 Track active users")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your data sources and try again.")