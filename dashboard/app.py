import json
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(page_title="Restaurant Ops Copilot Dashboard", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 22px !important;
    }
    h1 { font-size: 42px !important; }
    h2 { font-size: 30px !important; }
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 22px !important;
    }
    table {
        font-size: 22px !important;
    }
    .stJson {
        font-size: 22px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍽️ Restaurant Ops Copilot — Dashboard")

# --- Bookings ---
st.header("Tonight's Bookings")
with open(PROJECT_ROOT / "data" / "bookings.json") as f:
    bookings_data = json.load(f)

col1, col2 = st.columns(2)
col1.metric("Total Tables", bookings_data["total_tables"])
col2.metric("Total Bookings", len(bookings_data["bookings"]))
st.dataframe(bookings_data["bookings"], width='stretch')

# --- Inventory ---
st.header("Inventory Status")
with open(PROJECT_ROOT / "data" / "inventory.json") as f:
    inventory_data = json.load(f)

rows = []
for name, item in inventory_data.items():
    below_par = item["qty"] < item["par_level"]
    rows.append({
        "Ingredient": name,
        "Qty": item["qty"],
        "Unit": item["unit"],
        "Par Level": item["par_level"],
        "Status": "⚠️ Below Par" if below_par else "✅ OK",
    })
st.dataframe(rows, width='stretch')

# --- Agent Trace ---
st.header("Latest Agent Activity Log")
log_path = PROJECT_ROOT / "logs" / "agent_trace.jsonl"
if log_path.exists():
    lines = log_path.read_text().strip().split("\n")
    recent = lines[-10:]
    for line in recent:
        entry = json.loads(line)
        tool = entry["detail"].get("tool", "?")
        summary = f"**{entry['timestamp'][11:19]}** · `{entry['agent_name']}` · **{entry['event_type']}** · tool=`{tool}`"
        with st.expander(summary, expanded=False):
            st.json(entry)
else:
    st.info("No agent activity logged yet. Run `adk run agents/orchestrator_agent` first.")

# --- Eval Results ---
st.header("Latest Evaluation Results")
eval_path = PROJECT_ROOT / "evals" / "eval_results.json"
if eval_path.exists():
    eval_results = json.loads(eval_path.read_text())
    passed = sum(1 for r in eval_results if r["passed"])
    st.metric("Eval Pass Rate", f"{passed}/{len(eval_results)}")
    st.dataframe(
        [{"Case": r["id"], "Passed": "✅" if r["passed"] else "❌"} for r in eval_results],
        width='stretch',
    )
else:
    st.info("No eval results yet. Run `python evals/run_evals.py` first.")