from collections import Sequence

from itertools import groupby
from operator import itemgetter


def remove_duplicates_from_sorted_seq(seq: Sequence) -> Sequence:
    return tuple(map(itemgetter(0), groupby(seq)))
