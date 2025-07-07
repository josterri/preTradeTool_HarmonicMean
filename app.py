# app.py 

import streamlit as st
from spend_averages_tab import run_spend_averages_tab

st.set_page_config(page_title="Share Buyback Tool", layout="wide")
#st.title("📈 Share Buyback Tool")
import streamlit as st
from PIL import Image

# Load and display the local logo
logo = Image.open("candorLogo.jpg")
st.image(logo, width=300)

# Then add your title (below or above as you prefer)
st.title("📈  A Fixed-Notional Share Buyback Strategy")

# Add clickable link below
st.markdown("[www.candorpartners.net](https://www.candorpartners.net/)")
with st.sidebar:
    st.header("Simulation Settings")
    mc_horiz      = st.number_input("Horizon (days)",        50, 500, 125, step=5)
    mc_drift      = st.number_input("Avg price increase (annual, %)",      0, 100,   0, step=1)/100.0
    mc_vol        = st.number_input("Volatility (annual, %)", 0, 100,  25, step=1)/100.0
    initial_price = st.number_input("Initial Price (S₀)",     10, 1000,  100, step=10)
    mc_sims       = st.number_input("Simulations",          10000, 300000, 10000, step=10000)
#    total_shares  = st.number_input("Total Shares",            1, 1000000, 100, step=100)

    st.markdown("---")
    st.markdown(
            "Created by Joerg Osterrieder \n"
            "[www.joergosterrieder.com](https://www.joergosterrieder.com)",
            unsafe_allow_html=True
        )
tabs = st.tabs([
    "💲 Arithmetic vs Harmonic Mean"
])

with tabs[0]:
    run_spend_averages_tab(
        initial_price, mc_drift, mc_vol, mc_horiz, mc_sims, total_shares=100
    )
