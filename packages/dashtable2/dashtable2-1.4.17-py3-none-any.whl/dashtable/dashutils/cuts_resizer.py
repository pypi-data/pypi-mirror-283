from typing import Union, Sequence, Tuple

import numpy as np

from .aliases import array2D, Number, array1D


class CutsResizer:
    """
    Simple class provides operations to resize cuts sequences with keeping their relational intersections
    """
    def __init__(self, cuts: Union[array2D, Sequence[Tuple[Number, Number]]]):
        self.cuts = cuts if isinstance(cuts, np.ndarray) else np.array(cuts)

    def __repr__(self):
        return str(list(map(tuple, self.cuts.tolist())))

    def ensure_min_length(self, index: int, value: Number):
        """
        ensures whether the whole dimension for index have at least this length

        >>> c = CutsResizer([(1, 3), (4, 5), (3, 8), (6, 7)])
        >>> c.ensure_min_length(1, value=3); c
        [(1, 3), (4, 6), (3, 9), (7, 8)]
        >>> c.ensure_min_length(-1, value=5); c
        [(1, 3), (4, 6), (3, 12), (7, 11)]
        >>> c.ensure_min_length(0, 4); c
        [(1, 4), (5, 7), (4, 13), (8, 12)]
        """
        arr = self.cuts
        right = arr[index, 1]
        current = right - arr[index, 0] + 1
        if current >= value:
            return

        arr[arr >= right] += value - current

    # @profile
    def ensure_min_lens(self, lens: Union[array1D, Sequence[Number]]):
        """
        vectorized (fast) version of ensure_min_length for each cut

        >>> c = CutsResizer([(1, 3), (4, 5), (3, 8), (6, 7)])
        >>> c.ensure_min_lens([4, 3, 1, 1]); c
        [(1, 4), (5, 7), (4, 10), (8, 9)]
        >>> c.ensure_min_lens([4, 3, 1, 6]); c
        [(1, 4), (5, 7), (4, 14), (8, 13)]
        >>> c.ensure_min_lens([4, 4, 1, 6]); c
        [(1, 4), (5, 8), (4, 15), (9, 14)]
        """
        if not isinstance(lens, np.ndarray):
            lens = np.array(lens)

        arr = self.cuts
        assert lens.size == arr.shape[0], (lens.size, arr.shape[0])

        left = arr[:, 0]
        right = arr[:, 1]
        current = right - left + 1

        mask = current < lens
        indexes = np.where(mask)[0]
        while indexes.size:
            lens = lens[mask]
            current = current[mask]
            amax = lens.argmax()

            arr[arr >= arr[indexes[amax], 1]] += lens[amax] - current[amax]

            left = arr[indexes, 0]
            right = arr[indexes, 1]
            current = right - left + 1
            mask = current < lens
            indexes = indexes[mask]
