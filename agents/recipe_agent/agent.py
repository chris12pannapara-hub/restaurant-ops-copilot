import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from tools.inventory_tools import get_available_stock
from agents.search_agent.agent import root_agent as search_agent
from tools.logging_utils import before_tool_logger, after_tool_logger

RECIPE_INSTRUCTIONS = """
You are the Recipe Specialist Agent ("Get Inspired").

Your job is to propose 2-3 practical recipe ideas that fit the restaurant's
current stock and are informed by current food culture.

Workflow:
1. Call get_available_stock first and treat it as the hard constraint.
2. Use search_agent to gather evidence about:
   - current trending dishes or food styles
   - Michelin-star restaurant dishes or signature recipes
   - top chefs' cookbooks or chef-inspired recipes
3. Create ideas that are realistic for the restaurant and that match the
   available stock.
4. Respond with 2-3 concise dish ideas. For each idea, include:
   - dish name
   - why it fits the current stock
   - Source type: [Trending] or [Michelin-inspired] or [Chef Cookbook]
   - One-sentence evidence summary

Hard rule: NEVER suggest a dish that requires an ingredient not present in the
available stock result.
Hard rule: Never invent ingredients, quantities, or sources. If evidence is
weak or unavailable, say so clearly.
"""

root_agent = Agent(
    name="recipe_agent",
    model="gemini-2.5-flash",
    description="Suggests dishes using in-stock ingredients and live trend data, always citing a source.",
    instruction=RECIPE_INSTRUCTIONS,
    tools=[get_available_stock, AgentTool(agent=search_agent)],
    before_tool_callback=before_tool_logger,
    after_tool_callback=after_tool_logger,
)