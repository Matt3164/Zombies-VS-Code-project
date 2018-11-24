from typing import List

from pyzombies.utils.optimization.criteria import Criteria

class Max_Criteria(Criteria):
    """"""

    def sort(self, data_list: List) -> List:
        return sorted(data_list)[::-1]

    def _get_optimum_value(self, data_list: List):
        return max(data_list)

