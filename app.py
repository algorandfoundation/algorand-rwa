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
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Apply font globally */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    /* Tab/Pills styling to match your cyan theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #001324;
        color: #17cac6;
        border: 1px solid #001324;
        border-radius: 15px;
        font-size: 10px;
        padding: 10px 20px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #17CAC6;
        color: #001324;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #17cac6 !important;
        color: #001324 !important;
        font-weight: bold;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #001324;
        color: #17cac6;
        border: 1px solid #17cac6;
        border-radius: 15px;
        font-weight: bold;
        padding: 10px 20px;
    }
    
    .stButton > button:hover {
        background-color: #17cac6;
        color: #001324;
    }
    
/* Pills styling - Inactive state */
    button[data-testid="stBaseButton-pills"] {
        background-color: #001324 !important;
        color: #17cac6 !important;
        border: 1px solid #001324 !important;
        border-radius: 15px !important;
        padding: 8px 16px !important;
        margin: 2px !important;
    }
    
    button[data-testid="stBaseButton-pills"] p {
        color: #17cac6 !important;
        font-size: 14px !important;
    }
    
    /* Pills hover - Inactive state */
    button[data-testid="stBaseButton-pills"]:hover {
        background-color: #17CAC6 !important;
        border: 1px solid #17CAC6 !important;
    }
    
    button[data-testid="stBaseButton-pills"]:hover p {
        color: #001324 !important;
    }
    
    /* Pills styling - Active/Selected state */
    button[data-testid="stBaseButton-pillsActive"] {
        background-color: #17cac6 !important;
        color: #001324 !important;
        border: 1px solid #17cac6 !important;
        border-radius: 15px !important;
        padding: 8px 16px !important;
        margin: 2px !important;
    }
    
    button[data-testid="stBaseButton-pillsActive"] p {
        color: #001324 !important;
        font-size: 12px !important;
    }
    
    /* Pills hover - Active state (keep same styling) */
    button[data-testid="stBaseButton-pillsActive"]:hover {
        background-color: #17cac6 !important;
        border: 1px solid #17cac6 !important;
    }
    
    button[data-testid="stBaseButton-pillsActive"]:hover p {
        color: #001324 !important;
    }
    
    /* Header styling - keep white */
    h1 {
        color: #ffffff !important;
    }
    
    h2, h3 {
        color: #ffffff !important;
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

# Main title (centered, no button)
st.markdown("<h1 style='text-align: center; color: #ffffff;'>Algorand - Real World Assets Dashboard (preAlpha)</h1>", unsafe_allow_html=True)

st.markdown("---")

# Tabs with refresh button in the same row
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    st.write("")  # Spacer

with col2:
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Overview",
        "Micropayments",
        "Stablecoins",
        "Commodities",
        "Private Credit",
        "Real Estate",
        "Certificates",
        "Loyalty"
    ])

with col3:
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        with st.spinner("Running dbt pipeline..."):
            subprocess.run(["/Users/marc/Documents/algorand-rwa/.venv/bin/dbt", "run", "--project-dir", "rwa_dbt"], check=True)

        st.success("✅ dbt completed.")
        time.sleep(1)
        st.rerun()

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