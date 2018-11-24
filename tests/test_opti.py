import random

from pyzombies.utils.optimization.min_criteria import Min_Criteria
from pyzombies.utils.optimization.criteria_factory import criteria_factory
from pyzombies.utils.optimization.ordered_multi_criteria_optimizer import Ordered_Multi_Criteria_Optimizer

def generate_fake_data():

    return {
        "field_1": int(10*random.random()),
        "field_2": random.random(),
        "field_3": random.random()
    }

def generate_fake_data_list(n):

    return [generate_fake_data() for i in range(n)]


if __name__ == '__main__':

    data = generate_fake_data_list(25)

    print(data)

    criteria = Min_Criteria("field_1")

    print(criteria.filter(data))
    print(len(criteria.filter(data)))

    multi_opt = Ordered_Multi_Criteria_Optimizer(
        [
            Min_Criteria("field_1"),
            Min_Criteria("field_2"),
        ]
    )

    print(multi_opt.find(data))

    multi_opt = Ordered_Multi_Criteria_Optimizer(
        [
            criteria_factory("field_1", "min"),
            criteria_factory("field_2", "max"),
        ]
    )

    print(multi_opt.find(data))