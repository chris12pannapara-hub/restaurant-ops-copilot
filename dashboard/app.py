import json
import sys
from pathlib import Path

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(page_title="Restaurant Ops Copilot Dashboard", layout="wide")

st.markdown("""
    <style>
    html { zoom: 1.3; }
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

booking_counts = {}
for b in bookings_data["bookings"]:
    booking_counts[b["time"]] = booking_counts.get(b["time"], 0) + 1

fig_bookings = px.bar(
    x=list(booking_counts.keys()),
    y=list(booking_counts.values()),
    labels={"x": "Time Slot", "y": "Number of Bookings"},
    title="Bookings by Time Slot",
    color=list(booking_counts.values()),
    color_continuous_scale="Blues",
)
fig_bookings.update_layout(showlegend=False, coloraxis_showscale=False)

capacity_line = bookings_data["total_tables"]
fig_bookings.add_hline(
    y=capacity_line,
    line_dash="dash",
    line_color="red",
    annotation_text=f"Capacity ({capacity_line} tables)",
    annotation_position="top left",
)

st.plotly_chart(fig_bookings, width='stretch')

# --- Inventory ---
st.header("Inventory Status")
with open(PROJECT_ROOT / "data" / "inventory.json") as f:
    inventory_data = json.load(f)

ingredients = list(inventory_data.keys())
qty_values = [inventory_data[i]["qty"] for i in ingredients]
par_values = [inventory_data[i]["par_level"] for i in ingredients]

fig_inventory = go.Figure()
fig_inventory.add_trace(go.Bar(name="Current Qty", x=ingredients, y=qty_values, marker_color="#2ecc71"))
fig_inventory.add_trace(go.Bar(name="Par Level", x=ingredients, y=par_values, marker_color="#e74c3c"))
fig_inventory.update_layout(
    barmode="group",
    title="Inventory: Current Stock vs Par Level",
    xaxis_title="Ingredient",
    yaxis_title="Quantity (kg)",
)
st.plotly_chart(fig_inventory, width='stretch')

below_par_items = [k for k, v in inventory_data.items() if v["qty"] < v["par_level"]]
if below_par_items:
    st.warning(f"⚠️ Below par: {', '.join(below_par_items)}")

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
    total = len(eval_results)

    st.metric("Eval Pass Rate", f"{passed}/{total}")

    st.dataframe(
        [{"Case": r["id"], "Passed": "✅" if r["passed"] else "❌"} for r in eval_results],
        width='stretch',
    )
else:
    st.info("No eval results yet. Run `python evals/run_evals.py` first.")