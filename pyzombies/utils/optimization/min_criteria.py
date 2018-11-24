from typing import List

from pyzombies.utils.optimization.criteria import Criteria

class Min_Criteria(Criteria):
    """"""

    def sort(self, data_list: List) -> List:
        return sorted(data_list)

    def _get_optimum_value(self, data_list: List):
        return min(data_list)

