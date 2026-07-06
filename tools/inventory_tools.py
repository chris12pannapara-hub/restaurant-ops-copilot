import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "inventory.json"

def load_inventory() -> dict:
    with open(DATA_PATH) as f:
        return json.load(f)

def check_inventory(ingredient: str) -> dict:
    """Returns current stock info for a single ingredient.

    Args:
        ingredient: Name of the ingredient, e.g. "tomatoes".
    """
    inv = load_inventory()
    item = inv.get(ingredient.lower())
    if not item:
        return {"found": False, "reason": f"No record for '{ingredient}'."}
    below_par = item["qty"] < item["par_level"]
    return {"found": True, **item, "below_par": below_par}

def get_low_stock_report() -> dict:
    """Returns all ingredients currently below par level. Used by the
    Orchestrator to proactively flag shortages.
    """
    inv = load_inventory()
    low = {k: v for k, v in inv.items() if v["qty"] < v["par_level"]}
    return {"low_stock_items": low, "count": len(low)}

def get_available_stock() -> dict:
    """Returns only in-stock (qty > 0) ingredients. Used as input context
    for the Recipe Agent so it never suggests a zero-stock ingredient.
    """
    inv = load_inventory()
    return {k: v for k, v in inv.items() if v["qty"] > 0}