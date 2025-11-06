import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.private_credit import get_tvl_data
from charts.private_credit.charts import create_dep_chart, create_borrows_chart

st.set_page_config(page_title="ALGORAND RWA - Stablecoins", layout="wide")

def format_large_number(num):
    """Format large numbers with K, M, B suffixes"""
    if num >= 1_000_000_000:
        return f"${num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"${num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"${num/1_000:.1f}K"
    else:
        return f"${num:.0f}"

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_data(coin):
    """Fetch data with automatic 1-hour refresh"""
    with st.spinner("Retrieving fresh data..."):
        data = get_tvl_data(coin)
    return data


def render():
    # Calculate metrics
    borrows_df = fetch_data('algorand')
    lend = borrows_df.iloc[-1]['borrows']
    lend_delta = lend/borrows_df.iloc[-30]['borrows'] - 1

    deposit = borrows_df.iloc[-1]['tvl']
    deposit_delta = deposit/borrows_df.iloc[-30]['tvl'] - 1

    # First row with 4 columns
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label=f"Total Deposited",
            value=format_large_number(deposit),
            delta=f"{deposit_delta*100:.2f}%",
            border=True
        )

    with col2:
        st.metric(
            label="Total Borrowed",
            value=format_large_number(lend),
            delta=f"{lend_delta*100:.2f}%",
            border=True
        )


    st.divider()
    chart_options = {
        "total_deposited": "Deposits",
        "total_borrowed": "Borrows"
    }

    selection = st.pills(
        "Chart Type",
        options=chart_options.keys(),
        format_func=lambda option: chart_options[option],
        selection_mode="single",
        default="total_deposited",
        label_visibility="collapsed",
        key="pills_privatecredit"  # Add this
    )

    # Add description based on selection
    chart_descriptions = {
        "total_deposited": "Deposited amount to the lending pools.",
        "total_borrowed": "Total amount borrowed."
    }

    if selection:
        st.info(chart_descriptions[selection])
    
    # Main content area
    try:
        # Fetch and prepare data
        with st.spinner("Loading data..."):
            # Market Cap Data
            borrows_df['date'] = pd.to_datetime(borrows_df['date'])
            borrows_df = borrows_df[borrows_df['date'] >= pd.Timestamp.now() - pd.DateOffset(years=1)]

        # Display selected chart
        if selection == "total_deposited":
            fig = create_dep_chart(borrows_df)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(borrows_df)
        
        elif selection == "total_borrowed":
            fig = create_borrows_chart(borrows_df)
            st.plotly_chart(fig)
            
            # Optional: Show data table
            with st.expander("View Raw Data"):
                st.dataframe(borrows_df)
        
        else:
            st.info("👆 Please select a chart type above to view the data.")

    except NameError:
        # If fetch_data is not defined, show a placeholder
        st.error("⚠️ Data fetching function not found. Please ensure `fetch_data` is imported.")
        st.info("This dashboard requires the following constants to be defined: `MARKET_CAP`, `VOLUME`, `ACTIVE_WALLETS`")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your data sources and try again.")