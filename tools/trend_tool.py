def get_trending_dishes(cuisine_hint: str = "") -> dict:
    """Placeholder trend source. In Step 3 this becomes a real Google
    Search grounded call. For now returns a static citable dataset so
    the Recipe Agent has a source to cite.
    """
    return {
        "source": "mock_trend_dataset_v1",
        "trending": [
            "Margherita-style flatbread",
            "Grilled chicken with charred onion",
            "Pan-seared fish with herb crust",
            "Beef and onion skewers",
        ],
    }