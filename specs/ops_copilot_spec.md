# Restaurant Ops Copilot — Spec

## Agent Card: OrchestratorAgent

- Capabilities: check_booking_capacity, check_inventory, delegate_to_recipe_agent
- Input: natural language booking/inventory request
- Output: confirmation, alternate slot, or delegated recipe suggestion

## Agent Card: RecipeAgent

- Capabilities: suggest_dishes(stock, trend_data)
- Input: { "stock": {...}, "trigger": "chef_request" }
- Output: { "suggestions": [...], "source_cited": true }

## Scenarios

Scenario: Booking within capacity
Given 5 tables, 3 currently booked tonight
When a customer requests a table for 8pm for 4 people
Then OrchestratorAgent confirms the booking

Scenario: Booking exceeds capacity
Given 5 tables, 5 currently booked tonight
When a customer requests a table for 8pm
Then OrchestratorAgent rejects and suggests an alternate time slot

Scenario: Low stock recipe request
Given tomatoes and basil are in stock, but no mozzarella
When a chef asks "what can I cook tonight?"
Then RecipeAgent suggests dishes using only tomatoes/basil, not mozzarella,
and cites a trending source

Scenario: Recipe agent delegation
Given OrchestratorAgent receives a "get inspired" request
When it has no recipe capability itself
Then it delegates to RecipeAgent with current stock and returns the result
