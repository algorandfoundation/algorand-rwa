import streamlit as st
import pandas as pd
import sys
from pathlib import Path

def render():
    st.title("Frequently Asked Questions")
    
    # Introduction
    st.markdown("""
    Find answers to common questions about the metrics and data in this dashboard.
    """)
    
    st.markdown("---")
    
    with st.expander("What are Active Addresses?"):
        st.markdown("""
        **Active Addresses** are onchain wallets that have interacted at least once during 
        that month with the given application.
        
        This metric helps measure:
        - User engagement with the application
        - Monthly activity levels
        - Growth in active user base
        
        A wallet is counted as active if it performs any transaction with the application 
        during the calendar month.
        """)
    
    with st.expander("What are Micropayments?"):
        st.markdown("""
        **Micropayments** focus on ALGO and USDC payments which have a value of less than $250. 
        In addition to this, HAFN is also included as a micropayment method.
        
        This metric tracks:
        - ALGO payments < $250
        - USDC payments < $250
        - All HAFN transactions
        """)
    
    with st.expander("Which Stablecoins are tracked?"):
        st.markdown("""
        The stablecoins considered are:
        - **USDC** (USD Coin)
        - **USDT** (Tether)
        - **xUSD**
        - **goUSD**
        
        **Important**: The mints and burns are **not included** on the dashboard.
        """)
    
    with st.expander("What Commodities are included?"):
        st.markdown("""
        The assets considered are:
        
        **From Meld Gold:**
        - **GOLD$** - Tokenized gold
        - **SILVER$** - Tokenized silver
        
        **From ASA.Gold:**
        - **Gold** - Gold-backed tokens
        """)
    
    with st.expander("What is Private Credit based on?"):
        st.markdown("""
        Private Credit relies on **Folks Finance Lending** platform.
        
        This includes all lending and borrowing activities on the Folks Finance protocol.
        """)
    
    with st.expander("What is Real Estate based on?"):
        st.markdown("""
        Real Estate relies on **Lofty** platform.
        
        This includes all tokenized real estate activities and transactions on Lofty.
        """)
    
    with st.expander("What is Loyalty based on?"):
        st.markdown("""
        Loyalty relies on **WorldChess wcpp program**.
        
        This tracks all activities related to the WorldChess loyalty points and rewards program.
        """)
    
 