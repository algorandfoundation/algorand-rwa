import streamlit as st
from content.stablecoins import stablecoins
from content.real_estate import real_estate
from content.micropayments import micropayments
from content.commodities import commodities
from content.private_credit import private_credit
from content.cerificates import certificates
from content.loyalty import loyalty
from content.overview import overview
from content.card import card
from content.faq import faq 
import base64

import time
import subprocess
from streamlit_autorefresh import st_autorefresh

# Rerun app every 60 minutes
st_autorefresh(interval=60 * 60 * 1000, key="data_refresh")

# Page configuration
st.set_page_config(
    page_title="Algorand RWA Dashboard",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS to enhance the theme from config.toml
st.markdown("""
<style>
/* Make tab container horizontally scrollable on small screens */
.stTabs [data-baseweb="tab-list"] {
    display: flex;
    flex-wrap: wrap; /* allow wrapping */
    overflow-x: auto; /* allow horizontal scroll if needed */
    -webkit-overflow-scrolling: touch;
    justify-content: center;
}

/* Prevent hidden overflow on mobile */
.stTabs [data-baseweb="tab"] {
    flex: 1 1 auto;
    min-width: fit-content;
    white-space: nowrap;
}

/* Make sure the scrollbar is visible on small screens */
@media (max-width: 768px) {
    .stTabs [data-baseweb="tab-list"] {
        justify-content: flex-start;
        padding: 0 5px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 10px !important;
        padding: 6px 10px !important;
    }
    h1, h2, h3 {
        font-size: 90%;
        text-align: center;
    }
}
</style>
""", unsafe_allow_html=True)


# Main title (centered, no button)
st.markdown("<h1 style='text-align: center; color: #ffffff;'>Algorand - Real World Assets Dashboard (Beta)</h1>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("<div class='responsive-tabs'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([0.5, 7, 0.5])
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<style>
@media (max-width: 768px) {
    .responsive-tabs .block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
@media (max-width: 600px) {
    html, body, [class*="css"] {
        font-size: 14px;
    }
    .stButton > button {
        padding: 6px 10px !important;
        font-size: 12px !important;
    }
    h1 {
        font-size: 18px !important;
    }
}
</style>
""", unsafe_allow_html=True)


with col1:
    st.write("")  # Spacer

with col2:
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "Overview",
        "Micropayments",
        "Pera Wallet Card",
        "Stablecoins",
        "Commodities",
        "Private Credit",
        "Real Estate",
        "Certificates",
        "Loyalty",
        "FAQ"
    ])

with col3:
    st.write("")  # Spacer

# Render each tab
with tab1:
    st.header("Overview")
    overview.render()

with tab2:
    st.header("Micropayments")
    micropayments.render()

with tab3:
    st.header("Pera Wallet Card")
    card.render()

with tab4:
    st.header("Stablecoins")
    stablecoins.render()

with tab5:
    st.header("Commodities")
    commodities.render()

with tab6:
    st.header("Private Credit")
    private_credit.render()

with tab7:
    st.header("Real Estate")
    real_estate.render()

with tab8:
    st.header("Certificates")
    certificates.render()

with tab9:
    st.header("Loyalty")
    loyalty.render()

with tab10:
    faq.render()

