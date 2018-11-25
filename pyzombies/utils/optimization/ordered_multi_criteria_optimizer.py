from pyzombies.utils.optimization.criteria import Criteria
from typing import List
from pyzombies.utils.logger import logger


class Ordered_Multi_Criteria_Optimizer(object):
    """"""

    def __init__(self, criteria_list: List[Criteria]):
        """Constructor for Ordered_Multi_Criteria_Optimizer"""

        self._criteria_list = criteria_list

    def find(self, data_list: List):

        candidates = data_list

        logger.info("Candidates")

        for candidate in candidates:
            logger.info(candidate)

        logger.info("I have {}".format(len(candidates)))

        final_criteria = self._criteria_list[-1]

        criterias = self._criteria_list[:-1]

        for criteria in criterias:

            candidates = criteria.filter(candidates)

            logger.info("Remaining candidates {}".format(len(candidates)))

            if len(candidates)==1:
                break

        if len(candidates) > 1:

            candidates = final_criteria.select(candidates)

        assert len(candidates)==1, "More than one candidate remaining: {}".format(len(candidates))

        return candidates[0]

