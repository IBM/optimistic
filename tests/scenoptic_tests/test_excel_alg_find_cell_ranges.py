from typing import Tuple

from scenoptic.excel_alg_find_cell_ranges import FindCellRanges, FindCellRangesByTuples, AnalyzeCellRanges

mat0 = [
    # 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 0
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 1
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 2
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # 7
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # 8
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # 9
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 10
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 11
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 12
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 13
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 14
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 15
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 16
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]  # 17
]

mat1 = [
    # 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 0
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 1
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 2
    [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],  # 3
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # 7
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0],  # 8
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # 9
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 10
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 11
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 12
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 13
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 14
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 15
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],  # 16
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]  # 17
]


def run_all_find_cell_ranges():
    analyze_matrix(sheet="mat0", matrix=mat0)
    analyze_matrix(sheet="mat1", matrix=mat1)
    analyze_tuples(sheet="mat0", matrix=mat0)
    analyze_tuples(sheet="mat1", matrix=mat1)
    analyze()
    analyze(predicate_min_max_row)
    analyze(predicate_min_max_row, predicate_min_max_col)
    analyze(lambda c: 0 <= c[1] <= 5, lambda c: 13 <= c[2] <= 20)


def analyze_matrix(sheet, matrix):
    mat = [[matrix[i][j] for j in range(len(matrix[0]))] for i in range(len(matrix))]
    find = FindCellRanges(sheet=sheet,
                          matrix=mat)
    find.analyze(verbose=True)


def analyze_tuples(sheet, matrix):
    data = set()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                data.add((i, j))
    find = FindCellRangesByTuples(sheet=sheet,
                                  data=set(sorted(data, key=lambda t: (t[1], t[0]))))
    find.analyze(verbose=True)


def analyze(*predicates):
    mat = {'mat0': mat0, 'mat1': mat1}
    data = set()
    for sheet, m in mat.items():
        for i in range(len(m)):
            for j in range(len(m[0])):
                if m[i][j] == 1:
                    data.add((sheet, i, j))

    find = AnalyzeCellRanges(*predicates)
    cells, ranges = find.analyze_by_predicate(data)
    print(f'Cells {sorted([tuple(v.values()) for v in cells], key=lambda t: (t[0]))}')
    print(f'Ranges {sorted([tuple(v.values()) for v in ranges], key=lambda t: (t[0]))}')


def predicate_min_max_row(cell: Tuple[str, int, int]):
    min_row = 0
    max_row = 5
    return min_row <= cell[1] <= max_row


def predicate_min_max_col(cell: Tuple[str, int, int]):
    min_col = 13
    max_col = 20
    return min_col <= cell[2] <= max_col


def test_find_cell_ranges_by_matrix():
    """
    >>> analyze_matrix(sheet="mat0", matrix=mat0)
    [{'sheet': 'mat0', 'start_row': 0, 'start_col': 4, 'end_row': 17, 'end_col': 6}, {'sheet': 'mat0', 'start_row': 0, 'start_col': 7, 'end_row': 2, 'end_col': 8}, {'sheet': 'mat0', 'start_row': 0, 'start_col': 9, 'end_row': 3, 'end_col': 9}, {'sheet': 'mat0', 'start_row': 0, 'start_col': 10, 'end_row': 2, 'end_col': 16}, {'sheet': 'mat0', 'start_row': 1, 'start_col': 17, 'end_row': 1, 'end_col': 17}, {'sheet': 'mat0', 'start_row': 7, 'start_col': 7, 'end_row': 9, 'end_col': 15}, {'sheet': 'mat0', 'start_row': 15, 'start_col': 7, 'end_row': 17, 'end_col': 16}]
    >>> analyze_matrix(sheet="mat1", matrix=mat1)
    [{'sheet': 'mat1', 'start_row': 0, 'start_col': 4, 'end_row': 17, 'end_col': 6}, {'sheet': 'mat1', 'start_row': 0, 'start_col': 7, 'end_row': 2, 'end_col': 7}, {'sheet': 'mat1', 'start_row': 0, 'start_col': 8, 'end_row': 3, 'end_col': 10}, {'sheet': 'mat1', 'start_row': 0, 'start_col': 11, 'end_row': 2, 'end_col': 12}, {'sheet': 'mat1', 'start_row': 0, 'start_col': 13, 'end_row': 3, 'end_col': 15}, {'sheet': 'mat1', 'start_row': 0, 'start_col': 16, 'end_row': 2, 'end_col': 16}, {'sheet': 'mat1', 'start_row': 1, 'start_col': 17, 'end_row': 1, 'end_col': 17}, {'sheet': 'mat1', 'start_row': 7, 'start_col': 7, 'end_row': 9, 'end_col': 11}, {'sheet': 'mat1', 'start_row': 7, 'start_col': 12, 'end_row': 7, 'end_col': 12}, {'sheet': 'mat1', 'start_row': 7, 'start_col': 13, 'end_row': 9, 'end_col': 15}, {'sheet': 'mat1', 'start_row': 9, 'start_col': 12, 'end_row': 9, 'end_col': 12}, {'sheet': 'mat1', 'start_row': 15, 'start_col': 7, 'end_row': 17, 'end_col': 11}, {'sheet': 'mat1', 'start_row': 15, 'start_col': 12, 'end_row': 15, 'end_col': 12}, {'sheet': 'mat1', 'start_row': 15, 'start_col': 13, 'end_row': 17, 'end_col': 14}, {'sheet': 'mat1', 'start_row': 15, 'start_col': 15, 'end_row': 15, 'end_col': 16}, {'sheet': 'mat1', 'start_row': 17, 'start_col': 12, 'end_row': 17, 'end_col': 12}, {'sheet': 'mat1', 'start_row': 17, 'start_col': 15, 'end_row': 17, 'end_col': 16}]
    >>> analyze_tuples(sheet="mat0", matrix=mat0)
    [{'sheet': 'mat0', 'start_row': 0, 'start_col': 4, 'end_row': 17, 'end_col': 6}, {'sheet': 'mat0', 'start_row': 0, 'start_col': 7, 'end_row': 2, 'end_col': 8}, {'sheet': 'mat0', 'start_row': 0, 'start_col': 9, 'end_row': 3, 'end_col': 9}, {'sheet': 'mat0', 'start_row': 0, 'start_col': 10, 'end_row': 2, 'end_col': 16}, {'sheet': 'mat0', 'start_row': 1, 'start_col': 17, 'end_row': 1, 'end_col': 17}, {'sheet': 'mat0', 'start_row': 7, 'start_col': 7, 'end_row': 9, 'end_col': 15}, {'sheet': 'mat0', 'start_row': 15, 'start_col': 7, 'end_row': 17, 'end_col': 16}]
    >>> analyze_tuples(sheet="mat1", matrix=mat1)
    [{'sheet': 'mat1', 'start_row': 0, 'start_col': 4, 'end_row': 17, 'end_col': 6}, {'sheet': 'mat1', 'start_row': 0, 'start_col': 7, 'end_row': 2, 'end_col': 7}, {'sheet': 'mat1', 'start_row': 0, 'start_col': 8, 'end_row': 3, 'end_col': 10}, {'sheet': 'mat1', 'start_row': 0, 'start_col': 11, 'end_row': 2, 'end_col': 12}, {'sheet': 'mat1', 'start_row': 0, 'start_col': 13, 'end_row': 3, 'end_col': 15}, {'sheet': 'mat1', 'start_row': 0, 'start_col': 16, 'end_row': 2, 'end_col': 16}, {'sheet': 'mat1', 'start_row': 1, 'start_col': 17, 'end_row': 1, 'end_col': 17}, {'sheet': 'mat1', 'start_row': 7, 'start_col': 7, 'end_row': 9, 'end_col': 11}, {'sheet': 'mat1', 'start_row': 7, 'start_col': 12, 'end_row': 7, 'end_col': 12}, {'sheet': 'mat1', 'start_row': 7, 'start_col': 13, 'end_row': 9, 'end_col': 15}, {'sheet': 'mat1', 'start_row': 9, 'start_col': 12, 'end_row': 9, 'end_col': 12}, {'sheet': 'mat1', 'start_row': 15, 'start_col': 7, 'end_row': 17, 'end_col': 11}, {'sheet': 'mat1', 'start_row': 15, 'start_col': 12, 'end_row': 15, 'end_col': 12}, {'sheet': 'mat1', 'start_row': 15, 'start_col': 13, 'end_row': 17, 'end_col': 14}, {'sheet': 'mat1', 'start_row': 15, 'start_col': 15, 'end_row': 15, 'end_col': 16}, {'sheet': 'mat1', 'start_row': 17, 'start_col': 12, 'end_row': 17, 'end_col': 12}, {'sheet': 'mat1', 'start_row': 17, 'start_col': 15, 'end_row': 17, 'end_col': 16}]
    >>> analyze()
    Cells [('mat0', 1, 17), ('mat1', 1, 17), ('mat1', 7, 12), ('mat1', 9, 12), ('mat1', 15, 12), ('mat1', 17, 12)]
    Ranges [('mat0', 0, 4, 17, 6), ('mat0', 0, 7, 2, 8), ('mat0', 0, 9, 3, 9), ('mat0', 0, 10, 2, 16), ('mat0', 7, 7, 9, 15), ('mat0', 15, 7, 17, 16), ('mat1', 0, 4, 17, 6), ('mat1', 0, 7, 2, 7), ('mat1', 0, 8, 3, 10), ('mat1', 0, 11, 2, 12), ('mat1', 0, 13, 3, 15), ('mat1', 0, 16, 2, 16), ('mat1', 7, 7, 9, 11), ('mat1', 7, 13, 9, 15), ('mat1', 15, 7, 17, 11), ('mat1', 15, 13, 17, 14), ('mat1', 15, 15, 15, 16), ('mat1', 17, 15, 17, 16)]
    >>> analyze(predicate_min_max_row)
    Cells [('mat0', 1, 17), ('mat1', 1, 17)]
    Ranges [('mat0', 0, 4, 5, 6), ('mat0', 0, 7, 2, 8), ('mat0', 0, 9, 3, 9), ('mat0', 0, 10, 2, 16), ('mat1', 0, 4, 5, 6), ('mat1', 0, 7, 2, 7), ('mat1', 0, 8, 3, 10), ('mat1', 0, 11, 2, 12), ('mat1', 0, 13, 3, 15), ('mat1', 0, 16, 2, 16)]
    >>> analyze(predicate_min_max_row, predicate_min_max_col)
    Cells [('mat0', 1, 17), ('mat1', 1, 17)]
    Ranges [('mat0', 0, 13, 2, 16), ('mat1', 0, 13, 3, 15), ('mat1', 0, 16, 2, 16)]
    >>> analyze(lambda c: 0 <= c[1] <= 5, lambda c: 13 <= c[2] <= 20)
    Cells [('mat0', 1, 17), ('mat1', 1, 17)]
    Ranges [('mat0', 0, 13, 2, 16), ('mat1', 0, 13, 3, 15), ('mat1', 0, 16, 2, 16)]
    """


if __name__ == '__main__':
    run_all_find_cell_ranges()
