import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.clickhouse_client import run_query
from queries.loyalty.queries import TRANSACTIONS, ADDRESSES
from charts.loyalty.charts import create_transactions_chart, create_mau_chart

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
    rows, cols = fetch_data(TRANSACTIONS)
    tx_df = pd.DataFrame(rows, columns=cols)
    tx = tx_df.iloc[-1]['txn']
    tx_delta = tx/tx_df.iloc[-2]['txn'] - 1

    # Calculate metrics
    rows, cols = fetch_data(ADDRESSES)
    addr_df = pd.DataFrame(rows, columns=cols)
    addr = addr_df.iloc[-1]['monthly_unique_users']
    addr_delta = addr/addr_df.iloc[-2]['monthly_unique_users'] - 1

    # First row with 4 columns
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label=f"Total Transactions",
            value=format_large_number(tx),
            delta=f"{tx_delta*100:.2f}%",
            border=True
        )

    with col2:
        st.metric(
            label="Monthly Active Addresses",
            value=format_large_number(addr),
            delta=f"{addr_delta*100:.2f}%",
            border=True
        )

    st.divider()
    chart_options = {
        "transactions_loyalty": "Monthly Transactions",
        "active_users_loyalty": "Active Addresses"
    }

    selection = st.pills(
        "Chart Type",
        options=chart_options.keys(),
        format_func=lambda option: chart_options[option],
        selection_mode="single",
        default="transactions_loyalty",
        label_visibility="collapsed",
        key="pills_loyalty"  # Add this
    )

    # Add description based on selection
    chart_descriptions = {
        "transactions_loyalty": "The number of monthly transactions generated on-chain.",
        "active_users_loyalty": "The sum of monthly users that got into the loyalty program."
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
            addr_df['month'] = pd.to_datetime(addr_df['month'])
            addr_df = addr_df[addr_df['month'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

        # Display selected chart
        if selection == "transactions_loyalty":
            fig = create_transactions_chart(tx_df)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(tx_df)
        
        elif selection == "active_users_loyalty":
            fig = create_mau_chart(addr_df)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(addr_df)
        
        else:
            st.info("👆 Please select a chart type above to view the data.")

    except NameError:
        # If fetch_data is not defined, show a placeholder
        st.error("⚠️ Data fetching function not found. Please ensure `fetch_data` is imported.")
        st.info("This dashboard requires the following constants to be defined: `MARKET_CAP`, `VOLUME`, `ACTIVE_WALLETS`")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your data sources and try again.")