
from typing import Dict, Iterable, List, Optional

import numpy as np

from ..dashutils.aliases import array2D, DATA_SPANS
from ..dashutils.cuts_resizer import CutsResizer
from ..dashutils.profile import profile

from .aliases import DATA_TABLE, CELL_LOCATION


#region BOXES PREPROCESS

def _find_boxes_union_and_check(boxes: Iterable[CELL_LOCATION]) -> CELL_LOCATION:
    """
    >>> _ = _find_boxes_union_and_check
    >>> _([(1, 2, 3, 4), (5, 6, 7, 8), (0, 4, 0, 10)])
    (0, 2, 7, 10)
    """
    xmin, ymin, xmax, ymax = 10000000, 10000000, -1, -1

    for b in boxes:
        assert all(0 <= v == int(v) for v in b), b
        x1, y1, x2, y2 = b
        assert x1 <= x2, b
        assert y1 <= y2, b

        if x1 < xmin:
            xmin = x1

        if x2 > xmax:
            xmax = x2

        if y1 < ymin:
            ymin = y1

        if y2 > ymax:
            ymax = y2

    return xmin, ymin, xmax, ymax


def _normalize_and_fill_dict(
    box_to_text: Dict[CELL_LOCATION, str],
    empty_text: str = ''
) -> Dict[CELL_LOCATION, str]:
    """
    >>> _ = _normalize_and_fill_dict
    >>> _({(0, 1, 2, 2): '1', (1, 3, 2, 4): '2'})
    {(0, 1, 2, 2): '1', (1, 3, 2, 4): '2', (0, 0, 0, 0): '', (0, 3, 0, 3): '', (0, 4, 0, 4): '', (1, 0, 1, 0): '', (2, 0, 2, 0): ''}
    >>> _({(1, 1, 2, 2): '1', (1, 3, 2, 4): '2'})
    {(0, 0, 1, 1): '1', (0, 2, 1, 3): '2'}
    >>> _({(1, 1, 2, 2): '1', (1, 3, 3, 4): '2'})
    {(0, 0, 1, 1): '1', (0, 2, 2, 3): '2', (2, 0, 2, 0): '', (2, 1, 2, 1): ''}
    """

    #
    # find total table bounds
    #
    xmin, ymin, xmax, ymax = _find_boxes_union_and_check(box_to_text.keys())

    #
    # shift cells to start from 0
    #
    if 0 in (xmin, ymin):  # no shift
        dct = box_to_text.copy()
    else:  # shift to min == 0
        dct = {
            (x1 - xmin, y1 - ymin, x2 - xmin, y2 - ymin): s
            for (x1, y1, x2, y2), s in box_to_text.items()
        }
        xmax -= xmin
        ymax -= ymin
        # xmin = ymin = 0

    #
    # fill used cells map
    #
    done_cells = np.zeros((xmax + 1, ymax + 1), dtype=bool)
    for x1, y1, x2, y2 in dct.keys():
        sls = (slice(x1, x2 + 1), slice(y1, y2 + 1))
        if done_cells[sls].any():
            raise ValueError("cells intersections!")
        done_cells[sls] = True

    #
    # add empty cells
    #
    dct.update(
        {
            (x, y, x, y): empty_text
            for x, y in zip(*np.where(~done_cells))
        }
    )

    return dct

#endregion


#region ARRAY TRANSFORMATIONS

def _add_borders_to_coords(coords: array2D):
    """
    converts [start; end] coordinates in the way to provide borders between them;
        and these borders indexes must be common for close coords

    >>> _ = _add_borders_to_coords
    >>> r = np.array([(0, 0), (1, 1), (2, 2), (3, 3), (2, 4)])
    >>> _(r); r.tolist()
    [[0, 2], [2, 4], [4, 6], [6, 8], [4, 10]]
    """
    coords[:, 0] *= 2

    coords[:, 1] *= 2
    coords[:, 1] += 2


#endregion


#region TOOLS

def convert_table_spans_to_box_to_text(
    table: DATA_TABLE,
    spans: Optional[DATA_SPANS] = None,
) -> Dict[CELL_LOCATION, str]:
    """
    converts tables and spans (`data2rst` arguments) to `data2rst_enhanced` argument

    >>> _ = convert_table_spans_to_box_to_text
    >>> spans = [
    ...     [ [2, 1], [2, 2] ],
    ... ]
    >>> table = [
    ...     ["Header 1", "Header 2", "Header 3"],
    ...     ["body row 1", "column 2", "column 3"],
    ...     ["body row 2", "Cells may span columns.", ""],
    ... ]
    >>> _(table, spans)
    {(0, 0, 0, 0): 'Header 1', (0, 1, 0, 1): 'Header 2', (0, 2, 0, 2): 'Header 3', (1, 0, 1, 0): 'body row 1', (1, 1, 1, 1): 'column 2', (1, 2, 1, 2): 'column 3', (2, 0, 2, 0): 'body row 2', (2, 1, 2, 2): 'Cells may span columns.'}
    """

    dct = {
        (i, j, i, j): col
        for i, row in enumerate(table)
        for j, col in enumerate(row)
    }

    if spans:
        for lst in spans:
            lst = np.array(lst)
            for x, y in lst:
                dct.pop((x, y, x, y))
            xmin = lst[:, 0].min()
            xmax = lst[:, 0].max()
            ymin = lst[:, 1].min()
            ymax = lst[:, 1].max()
            dct[(xmin, ymin, xmax, ymax)] = table[xmin][ymin]

    return dct


#endregion

# @profile
def data2rst_enhanced(
    cell_box_to_text: Dict[CELL_LOCATION, str],
    missing_cell_value: str = ' '
) -> str:
    """
    produces almost same results as `data2rst` but much faster and robust
        because it uses completely different algorithm;
        preferred for using before html conversion;
        now this function is not customized to centerize texts and so on and maybe its not necessary

    Parameters
    ----------
    cell_box_to_text : dictionary { (row start, col start, row end, col end) -> cell string value };
        row/col ends must be included (use cuts [start; end] instead of [start;end) )
            and be integers >= 0; if all starts > 0 then the coordinates will be shifted to start from 0;
        it is not mandatory to provide all table cells including empty because they will be created automatically

    missing_cell_value : string value for missing cells


    Returns
    -------
        table view in rst format


    >>> def _run(cells: Iterable[CELL_LOCATION]):
    ...     cells = {b: str(b) for b in cells}
    ...     assert cells
    ...     print(data2rst_enhanced(cells))

    Simplest case:

    >>> _run([(0, 0, 0, 0), (1, 1, 1, 1)])
    +--------------+--------------+
    | (0, 0, 0, 0) |              |
    +--------------+--------------+
    |              | (1, 1, 1, 1) |
    +--------------+--------------+

    More heavy case:

    >>> _run([(0, 0, 0, 0), (1, 1, 1, 1), (0, 1, 0, 2), (1, 0, 2, 0)])
    +--------------+------------------+
    | (0, 0, 0, 0) | (0, 1, 0, 2)     |
    +--------------+--------------+---+
    | (1, 0, 2, 0) | (1, 1, 1, 1) |   |
    |              +--------------+---+
    |              |              |   |
    +--------------+--------------+---+

    This case cannot be performed by `data2rst`:

    >>> _run([(0, 0, 0, 0), (1, 2, 1, 2), (0, 1, 0, 2), (1, 0, 1, 1)])
    +--------------+----------------+
    | (0, 0, 0, 0) | (0, 1, 0, 2)   |
    +--------------+-+--------------+
    | (1, 0, 1, 1)   | (1, 2, 1, 2) |
    +----------------+--------------+

    Usual test:
    
    >>> spans = [
    ...     [ [3, 1], [4, 1] ],
    ...     [ [3, 2], [4, 2] ],
    ...     [ [2, 1], [2, 2] ],
    ... ]
    >>> table = [
    ...     ["Header 1", "Header 2", "Header 3"],
    ...     ["body row 1", "column 2", "column 3"],
    ...     ["body row 2", "Cells may span columns.", ""],
    ...     ["body row 3", "Cells may\\nspan rows.", "- Cells\\n- contain\\n- blocks."],
    ...     ["body row 4", "", ""],
    ... ]
    >>> print(data2rst_enhanced(convert_table_spans_to_box_to_text(table, spans)))
    +------------+------------+------------+
    | Header 1   | Header 2   | Header 3   |
    +------------+------------+------------+
    | body row 1 | column 2   | column 3   |
    +------------+------------+------------+
    | body row 2 | Cells may span columns. |
    +------------+------------+------------+
    | body row 3 | Cells may  | - Cells    |
    +------------+ span rows. | - contain  |
    | body row 4 |            | - blocks.  |
    +------------+------------+------------+

    """

    assert missing_cell_value, f"{missing_cell_value} must contain 1 char at least"

    # add missing cells to dict + check + transform strings
    dct: Dict[CELL_LOCATION, List[str]] = {
        b: (s or ' ').split('\n')
        for b, s in _normalize_and_fill_dict(cell_box_to_text, empty_text=missing_cell_value).items()
    }
    """
    dictionary { box -> list of strings per line}
    """

    #
    # extract cells boxes
    #
    boxes = np.array(list(dct.keys()))
    X = boxes[:, (0, 2)]
    Y = boxes[:, (1, 3)]

    #######################
    #
    # transform cells boxes
    #
    #######################

    # add borders to coordinates
    _add_borders_to_coords(X)
    _add_borders_to_coords(Y)

    #
    # fit lengths
    #
    Xc = CutsResizer(X)
    Yc = CutsResizer(Y)

    target_rows_cols = np.array(
        [
            (
                2 + len(lines),  # 2 is for borders
                4 + max(len(line) for line in lines)  # 4 is for 2 borders + 2 spaces
            )
            for i, lines in enumerate(dct.values())
        ]
    )
    """
    required rows and columns count for each cell
    
    this object is necessary for optimization purposes to not call too many shift operations
    """
    Xc.ensure_min_lens(target_rows_cols[:, 0])
    Yc.ensure_min_lens(target_rows_cols[:, 1])

    chars: array2D = np.full(
        (X[:, 1].max() + 1, Y[:, 1].max() + 1),
        fill_value=' ', dtype=object
    )
    """2D array of chars will be combined to one rst string"""

    nonempty_rows_mask = np.zeros(chars.shape[0], dtype=bool)
    """musk of non-empty table lines (which contain text or some cells corners)"""
    nonempty_cols_mask = np.zeros(chars.shape[1], dtype=bool)

    #
    # fill borders and texts
    #
    for (x1, x2), (y1, y2), lines in zip(X, Y, dct.values()):
        xs = slice(x1, x2 + 1)
        ys = slice(y1, y2 + 1)
        chars[x1, ys] = '-'
        chars[x2, ys] = '-'
        chars[xs, y1] = '|'
        chars[xs, y2] = '|'

        _y = y1 + 2
        """column where all lines will start"""
        _x = x1 + 1
        for i, line in enumerate(lines, _x):
            col_slice = slice(_y, _y + len(line))
            chars[i, col_slice] = list(line)
            nonempty_cols_mask[col_slice] = True
        nonempty_rows_mask[_x: _x + len(lines)] = True

    #
    # fill corners of all cells
    #

    for xpair, ypair in zip(X, Y):
        # for x, y in itertools.product(xpair, ypair):
        #     chars[x, y] = '+'
        chars[xpair[0], ypair] = '+'
        chars[xpair[1], ypair] = '+'

    Xu = np.unique(X.ravel())
    nonempty_rows_mask[Xu] = True
    Yu = np.unique(Y.ravel())
    nonempty_cols_mask[Yu] = True

    # mark cols around corners as nonempty too
    Yu -= 1
    nonempty_cols_mask[Yu[Yu >= 0]] = True
    Yu += 2
    nonempty_cols_mask[Yu[Yu < nonempty_cols_mask.size]] = True

    # #
    # # mark columns around nonempty as nonempty too
    # #
    # tmp1 = nonempty_cols_mask[:-1].copy()
    # tmp2 = nonempty_cols_mask[1:].copy()
    # nonempty_cols_mask[1:] |= tmp1
    # nonempty_cols_mask[:-1] |= tmp2

    return '\n'.join(
        ''.join(line[nonempty_cols_mask].tolist()) for line in chars[nonempty_rows_mask]
    )


def data2rst_v2(
    table: DATA_TABLE,
    spans: Optional[DATA_SPANS] = None,
    missing_cell_value: str = ' '
) -> str:
    """uses `data2rst_enhanced` for usual `data2rst` arguments"""
    return data2rst_enhanced(
        convert_table_spans_to_box_to_text(table, spans),
        missing_cell_value=missing_cell_value
    )








