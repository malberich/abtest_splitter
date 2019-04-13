"""
Experiment definition with 4 groups.

The split has been set unbalanced on purpose as it could help
spotting any issue that could appear detect any problem with
the randomness of the split.
"""
import os
import sys

sys.path.insert(
    0,
    "{}/src/splitter".format(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )
    )
)

import common

groups = [0 for id in range(0, 4)]

for value in range(1000000):
    group_assignment = common.get_split(
        "a{:06d}".format(value),
        [
            {
                'key': 1,
                'size': 70.0
            },
            {
                'key': 2,
                'size': 10.0
            },
            {
                'key': 3,
                'size': 10.0
            },
            {
                'key': 4,
                'size': 10.0
            }
        ]
    )
    groups[group_assignment] += 1

print(groups)
