"""
Utility helpers for TS EAMCET Portal.
"""
import pandas as pd
from src.config import CATEGORY_LABELS


def fmt_rank(rank: int | None) -> str:
    if rank is None:
        return "—"
    return f"{rank:,}"


def rank_label(rank: int) -> str:
    if rank <= 1_000:
        return "🏆 Excellent – Very High Chance"
    if rank <= 5_000:
        return "🥇 Very Good – High Chance"
    if rank <= 15_000:
        return "🥈 Good – Moderate Chance"
    if rank <= 40_000:
        return "🥉 Average – Fair Chance"
    if rank <= 80_000:
        return "⚠️ Below Average – Low Chance"
    return "❌ Difficult – Very Low Chance"


def rank_color(rank: int) -> str:
    if rank <= 1_000:  return "#16a34a"
    if rank <= 5_000:  return "#22c55e"
    if rank <= 15_000: return "#3b82f6"
    if rank <= 40_000: return "#f59e0b"
    if rank <= 80_000: return "#ef4444"
    return "#7f1d1d"


def fmt_tuition(val) -> str:
    try:
        v = int(val)
        return f"₹{v:,}"
    except (ValueError, TypeError):
        return "—"


def category_full(cat: str) -> str:
    return CATEGORY_LABELS.get(cat, cat)


def results_to_df(results: list[dict], show_tuition: bool = False) -> pd.DataFrame:
    """Convert search result list to a clean display DataFrame."""
    if not results:
        return pd.DataFrame()
    rows = []
    for i, r in enumerate(results, 1):
        row = {
            "#":            i,
            "Closing Rank": fmt_rank(r["rank"]),
            "College":      r["college"],
            "Branch":       r["branch"],
            "Place":        r["place"],
            "District":     r["dist"],
            "Type":         r["type"],
        }
        if show_tuition:
            row["Tuition Fee"] = fmt_tuition(r["tuition"])
        row["Affiliated To"] = r["affiliated"]
        rows.append(row)
    return pd.DataFrame(rows)


def to_csv(results: list[dict]) -> str:
    df = pd.DataFrame(results)
    return df.to_csv(index=False)
