"""
Filtering and lookup logic for TS EAMCET rank data.
All functions operate on a pre-loaded DataFrame.
"""
import pandas as pd
from src.config import (
    COL_COLLEGE, COL_BRANCH, COL_PLACE, COL_DIST,
    COL_TYPE, COL_TUITION, COL_AFFILIATED,
    RANK_COLS, CATEGORIES, BC_SUBTYPES, GENDERS,
)


# ── Dropdown population helpers ────────────────────────────────────────────

def get_colleges(df: pd.DataFrame) -> list[str]:
    if df.empty or COL_COLLEGE not in df.columns:
        return []
    return sorted(df[COL_COLLEGE].dropna().astype(str).unique().tolist())


def get_branches(df: pd.DataFrame, college: str | None = None) -> list[str]:
    if df.empty or COL_BRANCH not in df.columns:
        return []
    if college and college != "All Colleges":
        df = df[df[COL_COLLEGE] == college]
    return sorted(df[COL_BRANCH].dropna().astype(str).unique().tolist())


def get_rank_col(category: str, gender: str) -> str | None:
    return RANK_COLS.get((category, gender))


# ── Core lookup ────────────────────────────────────────────────────────────

def lookup_rank(df: pd.DataFrame, college: str, branch: str,
                category: str, gender: str) -> int | None:
    """Return the closing rank for a specific college+branch+cat+gender."""
    col = get_rank_col(category, gender)
    if col is None or col not in df.columns:
        return None
    mask = (df[COL_COLLEGE] == college) & (df[COL_BRANCH] == branch)
    rows = df[mask]
    if rows.empty:
        return None
    val = rows.iloc[0][col]
    try:
        v = int(val)
        return v if v > 0 else None
    except (ValueError, TypeError):
        return None


def lookup_row(df: pd.DataFrame, college: str, branch: str) -> pd.Series | None:
    """Return full row for a college+branch combination."""
    mask = (df[COL_COLLEGE] == college) & (df[COL_BRANCH] == branch)
    rows = df[mask]
    return rows.iloc[0] if not rows.empty else None


# ── Multi-result search ────────────────────────────────────────────────────

def search_ranks(df: pd.DataFrame, college: str | None, branch: str | None,
                 category: str, gender: str) -> list[dict]:
    """
    Search across all colleges/branches for the given category+gender.
    Returns list of dicts sorted by closing rank (ascending = better rank).
    """
    col = get_rank_col(category, gender)
    if col is None or col not in df.columns:
        return []

    filtered = df.copy()
    if college and college != "All Colleges":
        filtered = filtered[filtered[COL_COLLEGE] == college]
    if branch and branch != "All Branches":
        filtered = filtered[filtered[COL_BRANCH] == branch]

    results = []
    for _, row in filtered.iterrows():
        try:
            rank = int(row[col])
            if rank <= 0:
                continue
        except (ValueError, TypeError):
            continue

        results.append({
            "college":    str(row.get(COL_COLLEGE, "")),
            "branch":     str(row.get(COL_BRANCH, "")),
            "place":      str(row.get(COL_PLACE, "")),
            "dist":       str(row.get(COL_DIST, "")),
            "type":       str(row.get(COL_TYPE, "")),
            "tuition":    row.get(COL_TUITION),
            "affiliated": str(row.get(COL_AFFILIATED, "")),
            "category":   category,
            "gender":     gender,
            "rank":       rank,
        })

    results.sort(key=lambda x: x["rank"])
    return results


def get_rank_profile(df: pd.DataFrame, college: str, branch: str) -> dict:
    """
    Return all available ranks for a college+branch as a dict
    { 'OC Male': 12345, 'OC Female': 13000, ... } skipping nulls.
    """
    row = lookup_row(df, college, branch)
    if row is None:
        return {}
    profile = {}
    for (cat, gender), col in RANK_COLS.items():
        if col in df.columns:
            try:
                v = int(row[col])
                if v > 0:
                    profile[f"{cat} {gender}"] = v
            except (ValueError, TypeError):
                pass
    return profile


def compare_colleges(df: pd.DataFrame, branch: str,
                     category: str, gender: str) -> pd.DataFrame:
    """
    Return a DataFrame of all colleges offering `branch`,
    with their closing rank for category+gender, sorted best first.
    """
    col = get_rank_col(category, gender)
    if col is None or col not in df.columns:
        return pd.DataFrame()

    mask = df[COL_BRANCH] == branch
    sub  = df[mask].copy()
    sub["Closing Rank"] = pd.to_numeric(sub[col], errors="coerce")
    sub = sub[sub["Closing Rank"] > 0].sort_values("Closing Rank")

    out = sub[[COL_COLLEGE, COL_PLACE, COL_DIST, COL_TYPE,
               COL_TUITION, COL_AFFILIATED, "Closing Rank"]].copy()
    out.columns = ["College", "Place", "District", "Type",
                   "Tuition Fee", "Affiliated To", "Closing Rank"]
    out["Closing Rank"] = out["Closing Rank"].astype(int)
    return out.reset_index(drop=True)
