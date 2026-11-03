"""Core funnel metrics shared by the notebook and Power BI semantic model."""
import pandas as pd

STAGES = ["Visit", "Signup", "Activated", "Trial Started", "Paid"]

def funnel_table(fact: pd.DataFrame) -> pd.DataFrame:
    counts = fact.groupby("stage")["user_id"].nunique().reindex(STAGES)
    return pd.DataFrame({
        "users": counts,
        "step_conversion_pct": (100 * counts / counts.shift(1)).round(2),
        "cum_conversion_pct": (100 * counts / counts.iloc[0]).round(2),
    })

def by_segment(fact: pd.DataFrame, dim: pd.DataFrame, key: str) -> pd.DataFrame:
    seg = fact.merge(dim[["user_id", key]], on="user_id")
    out = seg.groupby([key, "stage"])["user_id"].nunique().unstack().reindex(columns=STAGES)
    out["visit_to_paid_pct"] = (100 * out["Paid"] / out["Visit"]).round(2)
    return out.sort_values("visit_to_paid_pct", ascending=False)
