import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.clickhouse_client import run_query
from queries.certificates.queries import CERTIFICATES, ADDRESSES
from charts.certificates.charts import create_certificates_chart, create_mau_chart

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
    rows, cols = fetch_data(CERTIFICATES)
    cert_df = pd.DataFrame(rows, columns=cols)
    cert = cert_df.iloc[-1]['total_certificates']
    cert_delta = cert/cert_df.iloc[-2]['total_certificates'] - 1

    # Calculate metrics
    rows, cols = fetch_data(ADDRESSES)
    addr_df = pd.DataFrame(rows, columns=cols)
    addr = addr_df.iloc[-1]['total_unique_addresses']
    addr_delta = addr/addr_df.iloc[-2]['total_unique_addresses'] - 1

    # First row with 4 columns
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label=f"Certificates Issued",
            value=format_large_number(cert),
            delta=f"{cert_delta*100:.2f}%",
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
        "certificates_issued": "Certificates Issued",
        "active_users": "Active Addresses"
    }

    selection = st.pills(
        "Chart Type",
        options=chart_options.keys(),
        format_func=lambda option: chart_options[option],
        selection_mode="single",
        default="certificates_issued",
        label_visibility="collapsed",
        key="pills_certificates"  # Add this
    )

    # Add description based on selection
    chart_descriptions = {
        "certificates_issued": "The number of monthly certificates issued on-chain.",
        "active_users": "The sum of monthly users that got an on-chain certificate."
    }

    if selection:
        st.info(chart_descriptions[selection])
    
    # Main content area
    try:
        # Fetch and prepare data
        with st.spinner("Loading data..."):
            # Market Cap Data
            cert_df['date'] = pd.to_datetime(cert_df['date'])
            cert_df = cert_df[cert_df['date'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

            # Volume Data
            addr_df['date'] = pd.to_datetime(addr_df['date'])
            addr_df = addr_df[addr_df['date'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

        # Display selected chart
        if selection == "certificates_issued":
            fig = create_certificates_chart(cert_df)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(cert_df)
        
        elif selection == "active_users":
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