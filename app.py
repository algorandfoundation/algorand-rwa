import streamlit as st
from content.stablecoins import stablecoins
from content.real_estate import real_estate
from content.micropayments import micropayments
from content.commodities import commodities
from content.private_credit import private_credit
from content.cerificates import certificates
from content.loyalty import loyalty

import time
import subprocess

# Page configuration
st.set_page_config(
    page_title="Asset Tokenization Dashboard",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to enhance the theme from config.toml
st.markdown("""
    <style>
    /* Tab/Pills styling to match your cyan theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #002a42;
        color: #ffffff;
        border: 1px solid #17cac6;
        border-radius: 4px;
        padding: 10px 20px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #0d8a87;
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #17cac6 !important;
        color: #001324 !important;
        font-weight: bold;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #17cac6;
        color: #001324;
        border: none;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #0d8a87;
        color: #ffffff;
    }
    
    /* Header styling - keep white */
    h1 {
        color: #ffffff !important;
    }
    
    h2, h3 {
        color: #17cac6 !important;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        color: #17cac6;
    }
    
    /* Divider color */
    hr {
        border-color: #17cac6;
    }
    </style>
""", unsafe_allow_html=True)

# Main title
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("<h1 style='text-align: center; color: #ffffff;'>Algorand - Real World Assets Dashboard</h1>", unsafe_allow_html=True)
with col2:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        with st.spinner("Running dbt pipeline..."):
            subprocess.run(["/Users/marc/Documents/algorand-rwa/.venv/bin/dbt", "run", "--project-dir", "rwa_dbt"], check=True)

        st.success("✅ dbt completed.")
        time.sleep(1)
        st.rerun()

st.markdown("---")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Overview",
    "💳 Micropayments",
    "💵 Stablecoins",
    "🌾 Commodities",
    "💰 Private Credit",
    "🏠 Real Estate",
    "📜 Certificates",
    "🎁 Loyalty"
])

# Render each tab
with tab1:
    st.header("Overview")
    #overview.render()

with tab2:
    st.header("Micropayments")
    micropayments.render()
    #overview.render()

with tab3:
    st.header("Stablecoins")
    stablecoins.render()
    #overview.render()

with tab4:
    st.header("Commodities")
    commodities.render()

with tab5:
    st.header("Private Credit")
    private_credit.render()

with tab6:
    st.header("Real Estate")
    real_estate.render()

with tab7:
    st.header("Certificates")
    certificates.render()

with tab8:
    st.header("Loyalty")
    loyalty.render()