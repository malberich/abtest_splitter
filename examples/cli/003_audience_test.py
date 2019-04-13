"""
Check whether that user fits into each given audience point.

The script keeps counting the users that got assigned to such level.
"""
import sys
import os

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

audience_buckets = [0 for id in range(0, 100)]

for value in range(10000):
    for audience in range(0, 100):
        if common.audience_filter(
            "b{:06d}".format(value),
            audience
        ) is True:
            audience_buckets[audience] += 1

for idx, a in enumerate(audience_buckets):
    print(
        "{}: {}".format(
            idx + 1,
            audience_buckets[idx]
        )
    )
