"""UUID-based splitting.

This test generates 1M UUIDv4 identifiers and splits them across
all the groups of the test with their corresponding percentage.

After the split the test shows the amount of users being assigned
to each group.

The total amount of users in each group is not fixed but it should
be probable enough to get a split with a 'similar enough' proportion
as configured on the groups.
"""
import os
import uuid
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

for i in range(1000000):
    value = str(uuid.uuid4())
    group_assignment = common.get_split(
        "{}".format(value),
        [
            {
                'key': 1,
                'size': 25.0
            },
            {
                'key': 2,
                'size': 25.0
            },
            {
                'key': 3,
                'size': 25.0
            },
            {
                'key': 4,
                'size': 25.0
            }
        ]
    )
    groups[group_assignment] += 1

print(groups)
