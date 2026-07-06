# 🍽️ Restaurant Ops Copilot

A multi-agent AI system built with **Google ADK** that helps restaurant staff manage
bookings, monitor inventory, and get AI-generated recipe inspiration grounded in
live food trends — while enforcing hard operational guardrails deterministically,
outside the LLM's control.

Built for the **Kaggle AI Agents: Intensive Vibe Coding Capstone Project** (Agents for Business track).

---

## Problem

Restaurant staff juggle bookings, inventory, and menu planning manually, often
reactively. This project explores whether a small, well-scoped multi-agent system
can proactively assist with these tasks — confirming bookings only within real
capacity, flagging low stock, and suggesting dishes chefs can actually cook tonight
using ingredients on hand and what's currently trending.

## Architecture

![Restaurant Ops Copilot Architecture](assets/architecture.png)

- **Orchestrator Agent** — owns booking and inventory tools, enforces the capacity
  guardrail, and delegates recipe requests to the Recipe Agent via ADK's native
  agent-to-agent transfer mechanism.
- **Recipe Agent** — reads current in-stock ingredients, calls the Search Agent for
  live trending dishes, Michelin-star restaurant recipes, and chef cookbooks, then
  suggests 2-3 ideas using only what's actually in stock.
- **Search Agent** — a dedicated agent wrapping Google Search grounding (ADK
  requires built-in tools to be isolated from custom function tools, hence the
  separate agent).

- **Orchestrator Agent** — owns booking and inventory tools, enforces the capacity
  guardrail, and delegates recipe requests to the Recipe Agent via ADK's native
  agent-to-agent transfer mechanism.
- **Recipe Agent** — reads current in-stock ingredients, calls the Search Agent for
  live trending dishes, and suggests 2-3 ideas using only what's actually in stock.
- **Search Agent** — a dedicated agent wrapping Google Search grounding (ADK
  requires built-in tools to be isolated from custom function tools, hence the
  separate agent).

## Concepts Demonstrated

| Concept                       | Where                                                                                                  |
| ----------------------------- | ------------------------------------------------------------------------------------------------------ |
| Multi-agent system            | 3 specialized agents, delegated via `transfer_to_agent` and `AgentTool`                                |
| Tools / function calling      | Custom Python tools for booking, inventory; Google Search grounding tool                               |
| Memory / session state        | Session-scoped context carries booking/stock state across a conversation                               |
| Agent-to-agent delegation     | Orchestrator → Recipe Agent → Search Agent chain, logged and verifiable                                |
| Spec-driven development       | `specs/ops_copilot_spec.md` (BDD/Gherkin) written before any code                                      |
| Evaluation-driven development | `evals/eval_cases.json` + `evals/run_evals.py`, 5/5 passing                                            |
| Security / guardrails         | Deterministic capacity + stock checks enforced outside the LLM                                         |
| Observability                 | `before_tool_callback`/`after_tool_callback` hooks logging every tool call to `logs/agent_trace.jsonl` |

## Guardrails (Security)

- `confirm_booking` **never** confirms a reservation exceeding table capacity —
  verified independently of what the LLM says.
- `get_available_stock` filters out zero-stock ingredients **before** the Recipe
  Agent ever sees them, preventing hallucinated suggestions using unavailable
  ingredients.
- No hardcoded credentials — API keys loaded exclusively via `.env` (excluded from
  version control).
- Mock data only — no real customer PII or payment data.

## Evaluation

5 test cases covering both guardrails, an inventory query, and multi-agent
delegation, defined as `Input → Expected Tool Calls → Expected Output` pairs
following Evaluation-Driven Development. Run with:

```bash
python evals/run_evals.py
```

Current result: **5/5 passing** (see `evals/eval_results.json`).

## Project Structure

restaurant-ops-copilot/
├── AGENTS.md # Global agent instructions/rules
├── specs/ops_copilot_spec.md # BDD spec written before implementation
├── data/ # Mock bookings + inventory
├── agents/
│ ├── orchestrator_agent/
│ ├── recipe_agent/
│ └── search_agent/
├── tools/ # Booking, inventory, logging utilities
├── evals/ # Eval cases + runner + results
├── dashboard/app.py # Streamlit operational dashboard
├── logs/sample_trace.jsonl # Sample audit trail
└── README.md

text

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file at the project root:
GOOGLE_API_KEY=your_key_from_aistudio.google.com
GOOGLE_GENAI_USE_VERTEXAI=FALSE

text

## Run It

Interactive CLI:

```bash
adk run agents/orchestrator_agent
```

Browser chat UI:

```bash
adk web
```

Operational dashboard:

```bash
streamlit run dashboard/app.py
```

Run evaluations:

```bash
python evals/run_evals.py
```

## Example Interaction

[user]: Book a table for 6 at 20:00
[orchestrator_agent]: Unfortunately, there are no tables left at 20:00.
We have availability at 19:00, 19:30, 21:00, 21:30, and 22:00.

[user]: What can I cook tonight?
[recipe_agent]: Based on live trending dishes and your current stock:

Honey Garlic Chicken with Roasted Tomatoes and Onions

Spicy Fish Tacos with Fresh Tomato and Basil Salsa

Rustic Beef and Onion Stir-fry with Fresh Basil

text

## Roadmap (Future Scope)

- Staff scheduling agent (cross-checking bookings vs. staff capacity)
- Real POS/reservation system integration via MCP
- Floor plan builder for front-of-house dashboard
- Content-to-booking flow (short-form video → reservation)
