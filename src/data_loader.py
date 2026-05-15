"""
Data loader for TS EAMCET Excel rank files.
Scans data/raw/, detects year and phase from filename, loads on demand.
"""
import os
import re
import pandas as pd
import streamlit as st
from src.config import PHASE_KEYWORDS, COL_COLLEGE, COL_BRANCH

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")


def _detect_year(filename: str) -> str | None:
    """Extract 4-digit year from filename."""
    m = re.search(r"(20\d{2})", filename)
    return m.group(1) if m else None


def _detect_phase(filename: str) -> str | None:
    """Detect counselling phase from filename keywords."""
    lower = filename.lower()
    for phase, keywords in PHASE_KEYWORDS.items():
        if any(k in lower for k in keywords):
            return phase
    return None


def _scan_files() -> dict:
    """
    Returns dict: { year: { phase: filepath } }
    Silently skips files that don't match the naming pattern.
    """
    catalog: dict = {}
    if not os.path.isdir(DATA_DIR):
        return catalog
    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.lower().endswith((".xlsx", ".xls")):
            continue
        year  = _detect_year(fname)
        phase = _detect_phase(fname)
        if not year or not phase:
            continue
        catalog.setdefault(year, {})[phase] = os.path.join(DATA_DIR, fname)
    return catalog


@st.cache_data(show_spinner=False)
def get_catalog() -> dict:
    return _scan_files()


def get_available_years() -> list[str]:
    return sorted(get_catalog().keys(), reverse=True)


def get_available_phases(year: str) -> list[str]:
    phase_order = ["First Phase", "Second Phase", "Final Phase"]
    available = list(get_catalog().get(year, {}).keys())
    return [p for p in phase_order if p in available]


@st.cache_data(show_spinner=False)
def load_df(year: str, phase: str) -> pd.DataFrame:
    """
    Load and clean the Excel file for the given year & phase.
    Returns an empty DataFrame on any error.
    """
    path = get_catalog().get(year, {}).get(phase)
    if not path:
        return pd.DataFrame()
    try:
        df = pd.read_excel(path, header=1, engine="openpyxl")
        # Drop completely empty rows
        df = df.dropna(how="all")
        # Drop footnote rows (no institution code = not real data)
        inst_col = "Inst\n Code"
        if inst_col in df.columns:
            df = df[df[inst_col].notna()]
        # Strip whitespace from string columns
        for col in [COL_COLLEGE, COL_BRANCH]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        # Drop rows where college or branch is empty/NaN
        df = df[df[COL_COLLEGE].str.strip() != ""]
        df = df[df[COL_BRANCH].str.strip()  != ""]
        # Add metadata columns for convenience
        df["_year"]  = year
        df["_phase"] = phase
        return df.reset_index(drop=True)
    except Exception as e:
        return pd.DataFrame()
