
import streamlit as st
import pandas as pd
import os, re

# ── Page config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TS EAMCET Rank Portal",
    page_icon="🎓",
    layout="centered",
)

# ── CSS — clean government-portal style ───────────────────────────────────
st.markdown("""
<style>
/* Import font */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans', Arial, sans-serif;
    background: #f5f5f5;
}

/* Hide Streamlit chrome */
#MainMenu, footer, .stDeployButton, header { visibility: hidden; }

/* Page header banner */
.portal-header {
    background: #1a3c6e;
    color: white;
    padding: 14px 20px;
    text-align: center;
    margin: -1rem -1rem 1.5rem -1rem;
    border-bottom: 4px solid #f4a012;
}
.portal-header h1 {
    font-size: 1.35rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: 0.02em;
}
.portal-header p {
    font-size: 0.85rem;
    margin: 4px 0 0 0;
    opacity: 0.88;
}

/* Form box */
.form-box {
    background: white;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    padding: 1.4rem 1.6rem 1rem 1.6rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
}
.form-title {
    font-size: 1rem;
    font-weight: 700;
    color: #1a3c6e;
    border-bottom: 2px solid #e8e8e8;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

/* Selectbox label */
.stSelectbox label {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #333 !important;
}
.st-af {
    font-size: 11px !important;
}
.stSelectbox > div > div {
    border: 1px solid #aaa !important;
    border-radius: 4px !important;
    font-size: 0.9rem !important;
}
/* No mobile keyboard popup */
.stSelectbox input {
    pointer-events: none !important;
    caret-color: transparent !important;
}

/* Submit button */
.stButton > button {
    background: #1a3c6e !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.6rem 2.5rem !important;
    cursor: pointer !important;
    transition: background 0.15s !important;
}
.stButton > button:hover {
    background: #15305a !important;
}

/* Results table — crisp on mobile (no WebGL) */
.result-wrap {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    background: white;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    margin-top: 1rem;
}
.result-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}
.result-table thead tr {
    background: #1a3c6e;
    color: white;
}
.result-table thead th {
    padding: 9px 11px;
    text-align: left;
    font-weight: 600;
    font-size: 0.78rem;
    white-space: nowrap;
    letter-spacing: 0.02em;
}
.result-table tbody tr:nth-child(even) { background: #f2f6fb; }
.result-table tbody tr:hover { background: #e6eef7; }
.result-table tbody td {
    padding: 8px 11px;
    border-bottom: 1px solid #e0e0e0;
    color: #1a1a1a;
    vertical-align: top;
    line-height: 1.4;
}
.result-table tbody td.rank-col {
    font-weight: 700;
    color: #1a3c6e;
    white-space: nowrap;
}
.result-table tbody td.sno-col {
    color: #666;
    white-space: nowrap;
}

/* Result count badge */
.result-count {
    background: #e8f0fb;
    border-left: 4px solid #1a3c6e;
    padding: 8px 14px;
    font-size: 0.88rem;
    color: #1a3c6e;
    font-weight: 600;
    border-radius: 0 4px 4px 0;
    margin-bottom: 0.5rem;
}

/* Note box */
.note-box {
    background: #fffbe6;
    border: 1px solid #f4d03f;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 0.8rem;
    color: #7d6608;
    margin-top: 1rem;
}

/* Footer */
.portal-footer {
    text-align: center;
    font-size: 0.75rem;
    color: #888;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #ddd;
}

@media (max-width: 600px) {
    .portal-header h1 { font-size: 1.1rem; }
    .result-table { font-size: 0.78rem; }
    .result-table thead th,
    .result-table tbody td { padding: 7px 8px; }
    .form-box { padding: 1rem 0.9rem 0.8rem; }
}
</style>
""", unsafe_allow_html=True)


# ── Constants ─────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")

RANK_COLS = {
    ("OC",   "Boys"):   "OC \nBOYS",
    ("OC",   "Girls"):  "OC \nGIRLS",
    ("BC_A", "Boys"):   "BC_A \nBOYS",
    ("BC_A", "Girls"):  "BC_A \nGIRLS",
    ("BC_B", "Boys"):   "BC_B \nBOYS",
    ("BC_B", "Girls"):  "BC_B \nGIRLS",
    ("BC_C", "Boys"):   "BC_C \nBOYS",
    ("BC_C", "Girls"):  "BC_C \nGIRLS",
    ("BC_D", "Boys"):   "BC_D \nBOYS",
    ("BC_D", "Girls"):  "BC_D \nGIRLS",
    ("BC_E", "Boys"):   "BC_E \nBOYS",
    ("BC_E", "Girls"):  "BC_E \nGIRLS",
    ("SC",   "Boys"):   "SC \nBOYS",
    ("SC",   "Girls"):  "SC \nGIRLS",
    ("ST",   "Boys"):   "ST \nBOYS",
    ("ST",   "Girls"):  "ST \nGIRLS",
    ("EWS",  "Boys"):   "EWS \nGEN OU",
    ("EWS",  "Girls"):  "EWS \nGIRLS OU",
}
CATEGORIES = ["OC", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E", "SC", "ST", "EWS"]
GENDERS    = ["Boys", "Girls"]

PHASE_ORDER = ["First Phase", "Second Phase", "Final Phase"]


# ── Data helpers ──────────────────────────────────────────────────────────
def detect_year(fname):
    m = re.search(r"(20\d{2})", fname)
    return m.group(1) if m else None

def detect_phase(fname):
    lower = fname.lower()
    if "final" in lower:         return "Final Phase"
    if "second" in lower:        return "Second Phase"
    if "first" in lower:         return "First Phase"
    return None

@st.cache_data(show_spinner=False)
def get_catalog():
    cat = {}
    if not os.path.isdir(DATA_DIR):
        return cat
    for f in sorted(os.listdir(DATA_DIR)):
        if not f.lower().endswith((".xlsx", ".xls")):
            continue
        y = detect_year(f)
        p = detect_phase(f)
        if y and p:
            cat.setdefault(y, {})[p] = os.path.join(DATA_DIR, f)
    return cat

@st.cache_data(show_spinner=False)
def load_df(year, phase):
    path = get_catalog().get(year, {}).get(phase)
    if not path:
        return pd.DataFrame()
    df = pd.read_excel(path, header=1, engine="openpyxl")
    df = df.dropna(how="all")
    inst_col = "Inst\n Code"
    if inst_col in df.columns:
        df = df[df[inst_col].notna()]
    for col in ["College Name", "Branch Name"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    df = df[df["College Name"].str.strip() != ""]
    df = df[df["Branch Name"].str.strip()  != ""]
    return df.reset_index(drop=True)


# ── Table renderer — plain HTML, crisp on mobile ──────────────────────────
def render_results(rows: list[dict]) -> None:
    header = "<th>S.No</th><th>College Name</th><th>Branch Name</th><th>Closing Rank</th>"
    body = ""
    for i, r in enumerate(rows, 1):
        body += (
            f"<tr>"
            f'<td class="sno-col">{i}</td>'
            f"<td>{r['college']}</td>"
            f"<td>{r['branch']}</td>"
            f'<td class="rank-col">{r["rank"]:,}</td>'
            f"</tr>"
        )
    st.markdown(
        f'<div class="result-wrap">'
        f'<table class="result-table">'
        f"<thead><tr>{header}</tr></thead>"
        f"<tbody>{body}</tbody>"
        f"</table></div>",
        unsafe_allow_html=True,
    )


# ── Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="portal-header">
  <h1>🎓 TS EAMCET / TG EAPCET — Closing Ranks</h1>
  <p>Telangana Engineering Admissions · All Colleges · All Categories</p>
</div>
""", unsafe_allow_html=True)


# ── Catalog ───────────────────────────────────────────────────────────────
catalog = get_catalog()
if not catalog:
    st.error("No rank files found in data/raw/. Please add the Excel files.")
    st.stop()

years  = sorted(catalog.keys(), reverse=True)
# ── Form ──────────────────────────────────────────────────────────────────
st.markdown('<div class="form-box"><div class="form-title">Opening and Closing Ranks</div>', unsafe_allow_html=True)

year = st.selectbox("Year", years)

phase_options = [p for p in PHASE_ORDER if p in catalog.get(year, {})]
phase = st.selectbox("Phase", phase_options)

# Load data for selected year+phase
df = load_df(year, phase)

if df.empty:
    st.error("Could not load data. Please check the Excel file.")
    st.stop()

# College dropdown — "All Colleges" first
colleges    = sorted(df["College Name"].dropna().unique().tolist())
college_sel = st.selectbox("College Name", ["-- All Colleges --"] + colleges)

# Branch dropdown — filtered by college if one selected
if college_sel != "-- All Colleges --":
    branch_df = df[df["College Name"] == college_sel]
else:
    branch_df = df
branches    = sorted(branch_df["Branch Name"].dropna().unique().tolist())
branch_sel  = st.selectbox("Branch Name (Academic Program)", ["-- All Branches --"] + branches)

# Category
cat_sel = st.selectbox("Category", CATEGORIES)

# Gender
gender_sel = st.selectbox("Gender", GENDERS)

submitted = st.button("Submit", type="primary")
st.markdown('</div>', unsafe_allow_html=True)  # close form-box

# ── Results ───────────────────────────────────────────────────────────────
if submitted:
    rank_col = RANK_COLS.get((cat_sel, gender_sel))

    if not rank_col or rank_col not in df.columns:
        st.error("Rank data not available for this category/gender combination.")
    else:
        filtered = df.copy()

        if college_sel != "-- All Colleges --":
            filtered = filtered[filtered["College Name"] == college_sel]

        if branch_sel != "-- All Branches --":
            filtered = filtered[filtered["Branch Name"] == branch_sel]

        # Build result rows sorted by closing rank
        results = []
        for _, row in filtered.iterrows():
            try:
                rank = int(row[rank_col])
                if rank > 0:
                    results.append({
                        "college": str(row["College Name"]),
                        "branch":  str(row["Branch Name"]),
                        "rank":    rank,
                    })
            except (ValueError, TypeError):
                continue

        results.sort(key=lambda x: x["rank"])

        if not results:
            st.warning("No data found for the selected filters. Please try a different combination.")
        else:
            count = len(results)
            st.markdown(
                f'<div class="result-count">Showing {count} result{"s" if count > 1 else ""} '
                f'— {cat_sel} · {gender_sel} · {phase} · {year}</div>',
                unsafe_allow_html=True,
            )
            render_results(results)

            # Download
            dl_df = pd.DataFrame(results)
            dl_df.columns = ["College Name", "Branch Name", "Closing Rank"]
            st.download_button(
                "⬇️  Download Results (CSV)",
                data=dl_df.to_csv(index=False),
                file_name=f"TSEAMCET_{year}_{phase}_{cat_sel}_{gender_sel}.csv",
                mime="text/csv",
            )

# ── Note ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="note-box">
  <strong>Note:</strong> Closing ranks shown are from the last round of the selected phase.
  Data is for reference only. Always verify with the official
  <a href="https://tsche.ac.in" target="_blank">TSCHE website</a>.
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="portal-footer">
  TS EAMCET / TG EAPCET Closing Ranks Portal &nbsp;·&nbsp;
  Data sourced from TSCHE official publications
</div>
""", unsafe_allow_html=True)
