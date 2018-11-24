from pyzombies.utils.optimization.max_criteria import Max_Criteria
from pyzombies.utils.optimization.min_criteria import Min_Criteria


MAX_CRITERIA_TAG="max"
MIN_CRITERIA_TAG="min"

CRITERIA_MAP=dict({
    MAX_CRITERIA_TAG: Max_Criteria,
    MIN_CRITERIA_TAG: Min_Criteria
})

def criteria_factory(field_name: str, criteria_tag: str):
    global CRITERIA_MAP
    return CRITERIA_MAP[criteria_tag](field_name)
