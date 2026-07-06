# Restaurant-Ops-Copilot

Agents for Business improving operational efficiency for restaurants

Security & Guardrails: The system enforces two deterministic guardrails outside the LLM's control: confirm_booking never confirms a reservation exceeding table capacity, and get_available_stock filters out zero-stock ingredients before the Recipe Agent ever sees them — preventing hallucinated bookings or recipe suggestions using unavailable ingredients. All tool calls are logged via before_tool_callback/after_tool_callback hooks to logs/agent_trace.jsonl, creating an auditable trace of every agent decision (the "Vibe Trajectory"). No API keys are hardcoded; credentials are loaded exclusively from environment variables via .env (excluded from version control). Mock data only is used — no real customer PII or payment data is processed.
