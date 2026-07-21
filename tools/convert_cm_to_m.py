from langchain.tools import tool

@tool
def convert_cm_to_m(distance: int) -> float:
    '''Converts the distance in centimeters to meters'''
    return distance/100