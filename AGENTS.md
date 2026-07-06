# AGENTS.md — Restaurant Ops Copilot

## Project

A multi-agent system (Google ADK, Python) that helps restaurant staff manage
bookings, inventory, and recipe inspiration.

## Stack

Python 3.11+, Google ADK, Streamlit (dashboard only), Gemini 2.5 Flash

## Hard Rules (Guardrails)

- NEVER confirm a booking that exceeds table/staff capacity.
- NEVER suggest a recipe using an ingredient with zero stock.
- All agent decisions must be logged to logs/agent_trace.jsonl.
- Mock data only — no real payments, no real customer PII.

## Agents

1. OrchestratorAgent — owns bookings + inventory tools, delegates recipe
   requests to RecipeAgent via a defined message schema (see specs/).
2. RecipeAgent — given stock + trending data, returns 2-3 dish suggestions,
   always cites a source (search result or dataset).

## Style

- snake_case for files, type hints everywhere, docstrings on all tool functions.
