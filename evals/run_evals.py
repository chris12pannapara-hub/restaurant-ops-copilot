import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from google.genai import types
from google.adk.runners import InMemoryRunner
from agents.orchestrator_agent.agent import root_agent

EVAL_FILE = Path(__file__).parent / "eval_cases.json"


async def run_case_async(case: dict, runner: InMemoryRunner) -> dict:
    user_id = "eval_user"
    session_id = f"eval_{case['id']}"

    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id,
    )

    message = types.Content(role="user", parts=[types.Part(text=case["input"])])

    final_text = ""
    tool_calls_made = []

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=message):
        if hasattr(event, "content") and event.content:
            for part in event.content.parts:
                if getattr(part, "text", None):
                    final_text += part.text
                if getattr(part, "function_call", None):
                    tool_calls_made.append(part.function_call.name)

    passed = True
    reasons = []

    for expected_tool in case.get("expected_tool_calls", []):
        if expected_tool not in tool_calls_made:
            passed = False
            reasons.append(f"Missing expected tool call: {expected_tool}")

    for phrase in case.get("expected_output_contains", []):
        if phrase.lower() not in final_text.lower():
            passed = False
            reasons.append(f"Output missing expected phrase: '{phrase}'")

    any_phrases = case.get("expected_output_contains_any", [])
    if any_phrases and not any(p.lower() in final_text.lower() for p in any_phrases):
        passed = False
        reasons.append(f"Output missing all of the acceptable phrases: {any_phrases}")

    for phrase in case.get("expected_output_not_contains", []):
        if phrase.lower() in final_text.lower():
            passed = False
            reasons.append(f"Output incorrectly contains forbidden phrase: '{phrase}'")

    return {
        "id": case["id"],
        "passed": passed,
        "reasons": reasons,
        "tool_calls_made": tool_calls_made,
        "output_snippet": final_text[:300],
    }


async def main_async():
    with open(EVAL_FILE) as f:
        cases = json.load(f)

    runner = InMemoryRunner(agent=root_agent, app_name="restaurant_ops_copilot")

    results = []
    for case in cases:
        result = await run_case_async(case, runner)
        results.append(result)

    print("\n=== EVAL RESULTS ===\n")
    passed_count = 0
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"[{status}] {r['id']}  | tool_calls: {r['tool_calls_made']}")
        if not r["passed"]:
            for reason in r["reasons"]:
                print(f"    - {reason}")
            print(f"    output_snippet: {r['output_snippet']!r}")
        passed_count += r["passed"]

    print(f"\n{passed_count}/{len(results)} eval cases passed.\n")

    Path("evals/eval_results.json").write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main_async())