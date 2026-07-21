from langchain.tools import tool

@tool
def calculate_total_cost(length: int, width: int, cost: int) -> float:
    '''Calculates the total cost of the service, using the length and width parameters, as well as per square meter cost'''
    return length * width * cost