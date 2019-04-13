"""
Test for the randomization with integer values.

Dispite the simplicity of an integer value serie, the random
assignment inside of each group should keep showing equilibrium.
"""
import hashlib

split_positions = [0 for i in range(0, 100)]

for i in range(10000):
    split_hash = int(
        hashlib.sha1(
            "{:010d}".format(i).encode('utf-8')
        ).hexdigest(),
        16
    )
    split_position = 100.0 * float(split_hash) / float(16 ** 40)
    split_positions[int(split_position)] += 1

print(split_positions)
