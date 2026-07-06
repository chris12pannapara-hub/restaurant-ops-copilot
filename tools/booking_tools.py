import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "bookings.json"

def load_bookings() -> dict:
    with open(DATA_PATH) as f:
        return json.load(f)

def check_booking_capacity(requested_time: str, party_size: int) -> dict:
    """Checks if a table is available at the requested time.

    Args:
        requested_time: Time in HH:MM format, e.g. "20:00".
        party_size: Number of guests.

    Returns:
        dict with 'available' (bool), 'reason' (str), and 'alternate_slots' (list).
    """
    data = load_bookings()
    total_tables = data["total_tables"]
    same_slot_bookings = [b for b in data["bookings"] if b["time"] == requested_time]

    if len(same_slot_bookings) < total_tables:
        return {"available": True, "reason": "Capacity available.", "alternate_slots": []}

    all_times = sorted(set(b["time"] for b in data["bookings"]))
    booked_counts = {t: sum(1 for b in data["bookings"] if b["time"] == t) for t in all_times}
    alternates = [t for t in all_times if booked_counts.get(t, 0) < total_tables]

    return {
        "available": False,
        "reason": f"No tables left at {requested_time} (capacity {total_tables}).",
        "alternate_slots": alternates,
    }


def confirm_booking(requested_time: str, party_size: int) -> dict:
    """Confirms a booking ONLY if capacity check passes. Enforces the
    hard rule from AGENTS.md: never confirm past capacity.
    """
    check = check_booking_capacity(requested_time, party_size)
    if not check["available"]:
        return {"confirmed": False, "detail": check}
    return {"confirmed": True, "detail": f"Table confirmed for {party_size} at {requested_time}."}