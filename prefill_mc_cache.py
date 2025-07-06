# prefill_cache.py

import itertools
from mcsimulation import load_or_run_simulation

def main():
    """
    Prefill the Monte Carlo cache (diskcache) over fine grids:
      • S₀ = 100
      • sims = 10_000
      • μ from -10% to +10% in 1% steps
      • σ from  0% to 100% in 1% steps
      • horizon = 1 to 252 days
    """
    S0           = 100.0
    sims         = 10_000
    total_shares = 100.0

    mu_list      = [i / 100.0 for i in range(-1, 1)]  
    sigma_list   = [i / 100.0 for i in range(0, 101)]   
    horizon_list = [i  for i in range(60, 300,5)]                  

    combos = itertools.product(mu_list, sigma_list, horizon_list)
    total  = len(mu_list) * len(sigma_list) * len(horizon_list)
    print(f"Prefilling cache with {total:,} runs…")

    for idx, (mu, sigma, horizon) in enumerate(combos, start=1):
        load_or_run_simulation(
            S0=S0,
            mu=mu,
            sigma=sigma,
            horizon=horizon,
            sims=sims,
            total_shares=total_shares
        )
        # progress every 10k or at end
        if idx % 1000 == 10 or idx == total:
            print(f"[{idx:,}/{total:,}] μ={mu:.2%}, σ={sigma:.2%}, h={horizon}")

    print("✅ Cache prefill complete.")

if __name__ == "__main__":
    main()
