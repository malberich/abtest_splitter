"""
Test the usage of the urandom to add more enthropy to the split.

The digest gets a value between 0 and 100.
"""
import binascii
import hashlib
import os

split_positions = [0 for i in range(0, 100)]

urand = binascii.hexlify(os.urandom(32)).decode()

for i in range(100000):
    split_hash = int(
        hashlib.sha1(
            "{}{:010d}".format(
                urand,
                i
            ).encode('utf-8')
        ).hexdigest(),
        16
    )
    split_position = 100.0 * float(split_hash) / float(16 ** 40)
    split_positions[int(split_position)] += 1

print(split_positions)
