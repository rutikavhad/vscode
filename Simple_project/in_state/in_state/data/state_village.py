def get_villages_by_state_tehsil(state_id: str, tehsil_id: str) -> dict:
    """
    Return villages dict for given state_id and tehsil_id.
    """

    try:
        module = __import__(
            f"in_state.data.villages.{state_id}",
            fromlist=["VILLAGES"]
        )
    except ImportError:
        raise ValueError(f"No village data found for state '{state_id}'")

    return module.VILLAGES.get(tehsil_id, {})
