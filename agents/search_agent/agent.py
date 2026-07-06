import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from google.adk.agents import Agent
from google.adk.tools import google_search
from tools.logging_utils import before_tool_logger, after_tool_logger

SEARCH_INSTRUCTIONS = """
You are a food trend research agent. When asked about trending dishes or
food styles near a location or in general, use google_search to find
current, real information. Always summarize findings concisely and mention
that the source is a live web search.
"""

root_agent = Agent(
    name="search_agent",
    model="gemini-2.5-flash",
    description="Searches the web for trending food/restaurant dishes using Google Search grounding.",
    instruction=SEARCH_INSTRUCTIONS,
    tools=[google_search],
    before_tool_callback=before_tool_logger,
    after_tool_callback=after_tool_logger,
)