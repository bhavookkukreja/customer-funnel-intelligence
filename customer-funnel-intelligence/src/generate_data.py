"""Generate synthetic WisprPro funnel data (30k users, May-Oct 2026).
Full reproducible pipeline lives in notebooks/funnel_analysis.ipynb.
Outputs: data/processed/fact_funnel.csv, dim_user.csv, data/funnel.db
"""
import numpy as np, pandas as pd

rng = np.random.default_rng(42)
N = 30_000
# Segment definitions (mult = relative conversion multiplier)
CHANNELS = ["Organic Search","Google Ads","Instagram","YouTube","Referral","LinkedIn"]
SIGNUP_MULT = {"Organic Search":1.00,"Google Ads":1.05,"Instagram":0.80,"YouTube":0.95,"Referral":1.35,"LinkedIn":1.15}
DEVICES = ["iOS","Android","Web","Windows","Mac"]
ACT_MULT = {"iOS":1.15,"Android":1.10,"Web":0.85,"Windows":1.00,"Mac":1.05}
PERSONAS = ["Creator","Developer","Student","Business","Support Agent"]
TRIAL_MULT = {"Creator":1.00,"Developer":1.10,"Student":0.85,"Business":1.30,"Support Agent":1.20}
PAID_MULT  = {"Creator":0.90,"Developer":1.10,"Student":0.70,"Business":1.50,"Support Agent":1.25}
PLAN_PRICE = {"Basic": 499, "Pro": 999, "Team": 1999}   # INR/month

if __name__ == "__main__":
    print("See notebooks/funnel_analysis.ipynb for the full data-generation walkthrough.")
