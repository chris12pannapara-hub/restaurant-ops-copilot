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
You are the Recipe Specialist Agent ("Get Inspired"). Given the restaurant's
current available stock (call get_available_stock) and trending dishes
(call search_agent for live trending food/dish ideas), suggest 2-3 dish ideas.

Hard rule: NEVER suggest a dish requiring an ingredient not present in the
available stock result. Always cite the trend source (mention it came from
a live web search via search_agent) in your answer.
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