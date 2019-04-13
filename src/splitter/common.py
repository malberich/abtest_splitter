import hashlib


def audience_filter(digest, audience):
    """Check whether the current audience level should include that digest."""
    return get_split(
        digest,
        [
            {
                "key": "audience_{}".format(idx),
                "size": 1.0
            } for idx in range(0, 100)
        ]
    ) < audience


def get_split(digest, groups):
    """Get the user's assignment to this test.

    :param str digest: String used for the hashing mechanism
    :param groups: List of candidate groups for the experiment
    :type groups: Array of groups
    """
    split_hash = int(
        hashlib.sha1(
            digest.encode('utf-8')
        ).hexdigest(),
        16
    )
    split_position = 100.0 * float(split_hash) / float(16 ** 40)

    group_threshold = 0.0
    for idx, group in enumerate(groups):
        group_threshold += float(group['size'])
        if split_position <= group_threshold:
            return idx
