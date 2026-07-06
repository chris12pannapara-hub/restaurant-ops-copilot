import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from google.adk.agents import Agent
from tools.booking_tools import check_booking_capacity, confirm_booking
from tools.inventory_tools import check_inventory, get_low_stock_report, get_available_stock
from agents.recipe_agent.agent import root_agent as recipe_agent
from tools.logging_utils import before_tool_logger, after_tool_logger

ORCHESTRATOR_INSTRUCTIONS = """
You are the Restaurant Ops Orchestrator. You handle booking requests and
inventory questions using your tools. You NEVER confirm a booking without
calling check_booking_capacity or confirm_booking first. If a user asks for
recipe ideas, cooking inspiration, or 'what can I cook', delegate to the
RecipeAgent by calling get_available_stock first, then transferring control.
Always be concise and cite tool results, don't guess numbers.
"""

root_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-flash",
    description="Handles restaurant booking and inventory operations.",
    instruction=ORCHESTRATOR_INSTRUCTIONS,
    tools=[check_booking_capacity, confirm_booking, check_inventory,
           get_low_stock_report, get_available_stock],
    sub_agents=[recipe_agent],
    before_tool_callback=before_tool_logger,
    after_tool_callback=after_tool_logger,
)