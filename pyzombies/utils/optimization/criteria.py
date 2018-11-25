from typing import List
from pyzombies.utils.logger import logger

class Criteria(object):
    """"""

    def __init__(self, field_name: str):
        """Constructor for Criteria"""
        self.field_name = field_name

    def get_field_value(self, data):
        return data[self.field_name]

    def extract_field_value_list(self, data_list: List)->List:

        return list(
            map(
                lambda data: self.get_field_value(data),
                data_list
            )
        )

    def _sort_values(self, values_list: List)->List:
        raise NotImplementedError

    def _get_optimum_value(self, values_list: List):
        raise NotImplementedError

    def filter(self, data_list: List)->List:

        values_list = self.extract_field_value_list(data_list)

        logger.info("Values for field {0}: {1}".format(self.field_name, list(set(values_list))))

        target_value = self._get_optimum_value(values_list)

        return list(
            filter(
                lambda data: self.get_field_value(data)==target_value,
                data_list
                )
        )

    def select(self, data_list: List):
        return self.filter(data_list)[:1]


