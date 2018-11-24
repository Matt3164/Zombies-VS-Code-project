from typing import List # needed

def argmin(value_list: List)->int:
    min_value = min(value_list)
    return value_list.index(min_value)

def argmax(value_list: List)->int:
    max_value = max(value_list)
    return value_list.index(max_value)