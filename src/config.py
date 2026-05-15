"""
Configuration constants for TS EAMCET Portal.
Column names match exactly what's in the Excel files.
"""

# ── Excel column names (exact) ─────────────────────────────────────────────
COL_INST_CODE   = "Inst\n Code"
COL_COLLEGE     = "College Name"
COL_PLACE       = "Place"
COL_DIST        = "Dist \nCode"
COL_CO_ED       = "Co Education"
COL_TYPE        = "College Type"
COL_YEAR_ESTAB  = "Year of Estab"
COL_BRANCH_CODE = "Branch Code"
COL_BRANCH      = "Branch Name"
COL_TUITION     = "Tuition Fee"
COL_AFFILIATED  = "Affiliated To"

# ── Rank columns ───────────────────────────────────────────────────────────
RANK_COLS = {
    ("OC",   "Male"):   "OC \nBOYS",
    ("OC",   "Female"): "OC \nGIRLS",
    ("BC_A", "Male"):   "BC_A \nBOYS",
    ("BC_A", "Female"): "BC_A \nGIRLS",
    ("BC_B", "Male"):   "BC_B \nBOYS",
    ("BC_B", "Female"): "BC_B \nGIRLS",
    ("BC_C", "Male"):   "BC_C \nBOYS",
    ("BC_C", "Female"): "BC_C \nGIRLS",
    ("BC_D", "Male"):   "BC_D \nBOYS",
    ("BC_D", "Female"): "BC_D \nGIRLS",
    ("BC_E", "Male"):   "BC_E \nBOYS",
    ("BC_E", "Female"): "BC_E \nGIRLS",
    ("SC",   "Male"):   "SC \nBOYS",
    ("SC",   "Female"): "SC \nGIRLS",
    ("ST",   "Male"):   "ST \nBOYS",
    ("ST",   "Female"): "ST \nGIRLS",
    ("EWS",  "Male"):   "EWS \nGEN OU",
    ("EWS",  "Female"): "EWS \nGIRLS OU",
}

# ── Categories ─────────────────────────────────────────────────────────────
CATEGORIES   = ["OC", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E", "SC", "ST", "EWS"]
BC_SUBTYPES  = ["BC_A", "BC_B", "BC_C", "BC_D", "BC_E"]
GENDERS      = ["Male", "Female"]

CATEGORY_LABELS = {
    "OC":   "OC – Open Category",
    "BC_A": "BC-A – Backward Classes A",
    "BC_B": "BC-B – Backward Classes B",
    "BC_C": "BC-C – Backward Classes C",
    "BC_D": "BC-D – Backward Classes D",
    "BC_E": "BC-E – Backward Classes E (Muslim)",
    "SC":   "SC – Scheduled Caste",
    "ST":   "ST – Scheduled Tribe",
    "EWS":  "EWS – Economically Weaker Section",
}

# ── File name patterns for year/phase detection ────────────────────────────
# Expected filename format: 01_TGEAPCET_2024_FirstPhase_LastRanks.xlsx
PHASE_KEYWORDS = {
    "First Phase":  ["first", "phase1", "phase_1", "1st"],
    "Second Phase": ["second", "phase2", "phase_2", "2nd"],
    "Final Phase":  ["final", "last", "finalphase"],
}
