# spend_averages_tab.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def run_spend_averages_tab(
    initial_price: float,
    mc_drift: float,
    mc_vol: float,
    mc_horiz: int,
    mc_sims: int,
    total_shares: float = 100
):
    """
    Tab: Compare arithmetic vs harmonic average of daily execution price
         under a fixed-notional (constant USD per day) strategy.
    """
#    st.markdown("## 📊 A Fixed-Notional Share Buyback Strategy")

    with st.expander("📘 Explanation: What This Simulation Shows"):
        st.markdown("This simulation compares two ways of measuring the average execution price under a **fixed-notional buyback strategy**, where the same dollar amount is spent each day.")
    
        st.markdown("### 🎯 Goal")
        st.markdown("To show that using the **arithmetic mean** of prices as a benchmark can be misleading. The **harmonic mean** more accurately reflects the true average execution price in this setting.")
    
        st.markdown("### 🔍 Method")
    
        st.markdown("You spend a **fixed amount** c per day (e.g. \\$100), so the number of shares bought on day t is:")
    
        st.latex(r"q_t = \frac{c}{p_t}")
    
        st.markdown("**Where:**")
        st.markdown("""
        - c: Constant daily dollar spend  
        - $p_t$: Price per share on day t 
        - $q_t$: Number of shares bought on day t
        """)
    
        st.markdown("The average execution price can be computed in two ways:")
    
        st.markdown("**1. Arithmetic Mean of Prices:**")
        st.latex(r"\overline{p}_{\rm arith} = \frac{1}{H} \sum_{t=1}^{H} p_t")
    
        st.markdown("**2. Harmonic Mean of Prices:**")
        st.latex(r"\overline{p}_{\rm harm} = \left( \frac{1}{H} \sum_{t=1}^{H} \frac{1}{p_t} \right)^{-1}")
    
        st.markdown("Only the **harmonic mean** properly accounts for varying shares bought each day under fixed spending.")
    
        st.markdown("---")
        st.markdown("### 🧾 Example")
    
        st.markdown("Assume you spend c = \\$100 each day for 3 days at the following prices:")
    
        st.latex(r"p_1 = 80,\quad p_2 = 100,\quad p_3 = 120")
    
        st.markdown("The shares you buy each day are:")
    
        st.latex(r"""
        q_1 = \frac{100}{80} = 1.25, \quad
        q_2 = \frac{100}{100} = 1.00, \quad
        q_3 = \frac{100}{120} \approx 0.83
        """)
    
        st.markdown("Total shares bought: $q_{total} = 1.25 + 1.00 + 0.83 = 3.08$")
    
        st.markdown("Total amount spent: $300. So your **true average execution price** is:")
    
        st.latex(r"\frac{300}{3.08} \approx 97.40")
    
        st.markdown("Now compare with the arithmetic and harmonic averages of the prices:")
    
        st.latex(r"\overline{p}_{\rm arith} = \frac{80 + 100 + 120}{3} = 100")
        st.latex(r"""
        \overline{p}_{\rm harm}
        = \left( \frac{1}{3} \left( \frac{1}{80} + \frac{1}{100} + \frac{1}{120} \right) \right)^{-1}
        \approx 97.40
        """)
    
        st.markdown("✅ The **harmonic mean** matches your actual cost per share. The **arithmetic mean** overstates it.")
    

        st.markdown("---")
    
        st.markdown("### ✅ Key Insight")
    
        st.markdown("""
        The **harmonic mean** correctly reflects the average execution price when spending a fixed dollar amount daily.  
        The **arithmetic mean** overweights high prices and should not be used as a benchmark in this strategy.
        """)
    
        
    st.markdown("# Calculations")

    # --- Input summary ---
    st.markdown(
        f"**Inputs:**  S₀ = ${initial_price:.0f}  |  "
        f"Avg price increase (annual) = {mc_drift:.0%}  |  "
        f"Volatility (annual) = {mc_vol:.0%}  |  "
        f"Horizon = {mc_horiz} days  |  "
        f"Simulations = {mc_sims:,}  |  "
   #     f"Total Shares = {total_shares:,}"
    )

    # --- 1) Simulate GBM price paths ---
    mu_d, sigma_d = mc_drift / 252.0, mc_vol / np.sqrt(252.0)
    Z    = np.random.normal(size=(mc_horiz, mc_sims))
    logs = np.vstack([
        np.zeros(mc_sims),
        np.cumsum((mu_d - 0.5 * sigma_d**2) + sigma_d * Z, axis=0)
    ])
    price_paths = initial_price * np.exp(logs)

    # --- 2) Compute per-day execution prices and their averages ---
    daily_prices = price_paths[1:]                # shape (H, sims)
    arith_price  = daily_prices.mean(axis=0)      # arithmetic mean per sim
    harm_price   = mc_horiz / (1.0 / daily_prices).sum(axis=0)

    # --- 3) Compute basis-point differences ---
    delta_bps = (arith_price - harm_price) / arith_price * 1e4

    # --- 4) Display metrics and histogram ---
    st.subheader("Average Difference in Execution Prices: Arithmetic vs Harmonic Mean ")
    
    
    delta_mean = delta_bps.mean()
    delta_std = delta_bps.std()
    n_sims = mc_sims
    mc_error = 2*delta_std / np.sqrt(n_sims)
    
    st.metric(
        label="Average execution price difference (bps)",
        value=f"{delta_mean:.1f} bps ± {mc_error:.1f} bps"
    )
    st.markdown(f"*Note: The estimated basis-point difference is valid for these specific parameters — annual avg pct price increase {mc_drift:.0%}, annual volatility {mc_vol:.0%}, and horizon {mc_horiz} days — and will change if any of them are modified.*")

    st.markdown("""
    *The ± error bar reflects the standard error due to a finite number of simulations and changes with the number of simulations.*
    """)
    df_hist = pd.DataFrame({"Δ in bps": delta_bps})
    fig = px.histogram(
        df_hist,
        x="Δ in bps",
        nbins=250,
        title="Difference in Execution Prices: Arithmetic vs. Harmonic Mean"
    )
    fig.update_layout(
    xaxis_title="Difference in Execution Price (Arithmetic − Harmonic) [bps]",
    yaxis_title="Number of Simulations"
    )   
    
    st.plotly_chart(fig, use_container_width=True)

    
    
    
    with st.expander("### 📈 Interpretation of Results"):
        delta_mean = delta_bps.mean()
        delta_std = delta_bps.std()
        st.markdown(f"""
        This chart shows the distribution of **basis-point differences** between the **arithmetic** and **harmonic** mean execution prices across all Monte Carlo simulations.
        
        - **Δ (bps)** represents how much higher the arithmetic mean is compared to the harmonic mean, on average across all simulations.
        - A value of **{delta_mean:.1f} bps** means that, on average, the arithmetic mean overstates the effective execution price by **{delta_mean/100:.1f} %**.
        - The **standard deviation of {delta_std:.1f} bps** indicates large variability across simulations.
        
        ---
        
        ### 💡 Key Takeaways
        
        - The **harmonic mean** is consistently **lower** than the arithmetic mean due to the nature of fixed-dollar execution: you buy **more shares when prices are low** and **fewer shares when prices are high**, which the harmonic mean accounts for.
        - Using the arithmetic mean as a performance benchmark can **overstate execution quality** by {delta_mean:.1f} basis points on average.
        - The long right tail in the histogram shows that in some scenarios, the overstatement can exceed **{delta_std*3:.1f} bps to {delta_std*4:.1f} bps and more**, especially in volatile price paths.
        
        ---
        
        ### ✅ Conclusion
        
        In fixed-notional buyback strategies, the **harmonic mean** is the correct benchmark.  
        **Outperforming the arithmetic mean does not imply execution skill** — it simply reflects the mechanical advantage built into the strategy.
        """)
        
        
        # --- Basis-Point Comparison ---
        st.markdown("### 📏 Difference in Execution Prices in bps")
        
        st.latex(r"""
        \Delta_{\mathrm{bps}} =
        \frac{\overline{p}_{\mathrm{arith}} - \overline{p}_{\mathrm{harm}}}
             {\overline{p}_{\mathrm{arith}}}
        \times 10{,}000
        """)
        
        st.markdown("""
        This formula measures the **relative difference** between the arithmetic and harmonic mean execution prices, expressed in **basis points (bps)**.
        
        - A **positive** \\( $\\Delta_{\\mathrm{bps}}$ \\) means the **harmonic mean is lower**, which reflects better execution pricing than the arithmetic average suggests.
        - A **negative** \\( $\\Delta_{\\mathrm{bps}}$ \\) means the **harmonic mean is higher**, indicating that your effective execution price was worse than the arithmetic benchmark.
        
           """)
    
    

    # --- 5) (Optional) show sample price paths ---
    st.subheader("Sample GBM Price Paths")
    st.markdown("Below are up to 100 simulated price trajectories:")
    max_plot = min(mc_sims, 100)
    df_paths = (
        pd.DataFrame(price_paths[:, :max_plot])
          .reset_index()
          .melt(id_vars="index", var_name="Simulation", value_name="Price")
          .rename(columns={"index": "Day"})
    )
    fig2 = px.line(
        df_paths,
        x="Day",
        y="Price",
        color="Simulation",
        line_group="Simulation",
        title=f"GBM Paths (showing {max_plot} of {mc_sims:,})"
    )
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
