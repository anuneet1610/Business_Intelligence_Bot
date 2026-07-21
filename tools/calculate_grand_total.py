from langchain.tools import tool

@tool
def calculate_grand_total(totals: list[float]) -> float:
    """Sums a list of item totals to get the grand total."""
    return sum(totals)
