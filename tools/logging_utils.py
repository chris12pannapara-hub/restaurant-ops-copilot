import json
import datetime
from pathlib import Path

LOG_PATH = Path(__file__).parent.parent / "logs" / "agent_trace.jsonl"
LOG_PATH.parent.mkdir(exist_ok=True)


def log_event(event_type: str, agent_name: str, detail: dict) -> None:
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "event_type": event_type,
        "agent_name": agent_name,
        "detail": detail,
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


def before_tool_logger(tool, args, tool_context):
    log_event("before_tool_call", tool_context.agent_name, {"tool": tool.name, "args": args})
    return None  # returning None lets the tool call proceed normally


def after_tool_logger(tool, args, tool_context, tool_response):
    log_event(
        "after_tool_call",
        tool_context.agent_name,
        {"tool": tool.name, "args": args, "response": tool_response},
    )
    return None  # returning None keeps the original response