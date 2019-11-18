# backtracking exercise

#####################################
#               sudoku              #
#####################################


def solve_sudoku(board):
    """
    :param board: list of lists that represent the sudoku board
    :return: True if the board can be solved, else False
    """
    zero_list = create_zero_list(board)     # list of empty cells indices
    cell_idx = 0
    sudoku_backtracking(board, zero_list, cell_idx)
    for cell in zero_list:
        i, j = cell
        if board[i][j] == 0:
            return False    # sudoku can't be solved
    return True


def sudoku_backtracking(board, zero_list, cell_idx):
    """
    :param board:
    :param zero_list:
    :param cell_idx:
    :return: True if the board can be solved, else False
    """
    if cell_idx == len(zero_list):                     # sudoku is solved
        return True
    i, j = zero_list[cell_idx]
    for num in range(1, len(board)+1):                   # all possible values for sudoku
        board[i][j] = num
        if is_num_valid(board, num, zero_list[cell_idx]):     # not in line/column/block
            if sudoku_backtracking(board, zero_list, cell_idx + 1):
                return True
    board[i][j] = 0
    return False


def create_zero_list(board):
    """
    :param board:
    :return: list of indices, where cell value is zero (empty cell)
    """
    zero_list = []
    n = len(board)          # num of lines
    for i in range(n):      # for each line
        for j in range(n):  # for each cell
            if board[i][j] == 0:
                cell = (i, j)
                zero_list.append(cell)
    return zero_list


def is_num_in_line(board, num, line):
    """
    :param board:
    :param num:
    :param line:
    :return: True if num is already in line, else False
    """
    if board[line].count(num) > 1:
        return True
    return False


def is_num_in_column(board, num, column):
    """
    :param board:
    :param num:
    :param column:
    :return: True if num is already in column, else False
    """
    n = len(board)          # num of lines/columns
    count = 0
    for line in range(n):
        if board[line][column] == num:
            count += 1
        if count == 2:  # the num already appears in column
            return True
    return False


def is_num_in_block(board, num, start_cell):
    """
    :param board:
    :param num:
    :param start_cell: first cell in block (top left)
    :return: True if num is already in block, else False
    """
    start_i, start_j = start_cell
    block_len = int(len(board) ** 0.5)
    count = 0
    for i in range(block_len):
        for j in range(block_len):
            if count == 2:
                return True
            if board[start_i + i][start_j + j] == num:
                count += 1
    if count == 2:
        return True
    return False


def find_start_cell_of_block(board, cell):
    """
    :param board:
    :param cell:
    :return: fins start cell = first cell in block (top left)
    """
    i, j = cell
    block_len = int(len(board) ** 0.5)
    i_diff = i % block_len
    j_diff = j % block_len
    start_cell = (i - i_diff, j - j_diff)
    return start_cell


def is_num_valid(board, num, cell):
    """
    :param board:
    :param num:
    :param cell:
    :return: True if num is valid, else False
    """
    i, j = cell
    if not is_num_in_line(board, num, i):
        if not is_num_in_column(board, num, j):
            if not is_num_in_block(board, num, find_start_cell_of_block(board, cell)):
                return True
    return False


#####################################
#            k subsets              #
#####################################

# k_subset 1
def print_k_subsets(n, k):
    """
    :param n: set size
    :param k: subsets length
    :return: prints all subsets
    """
    if k <= n:
        subset = [False] * n    # initializing list
        subset_helper(subset, k, 0, 0)


def subset_helper(subset, k, index, picked):
    """
    :param subset: list of current subset. True for chosen idx, else False.
    :param k:
    :param index: current idx
    :param picked: num of picked indices (num of True values in list) <= k
    :return: find out all possible subsets
    """
    if picked == k:     # k items where picked, print and backtrack
        print_subset(subset)
        return

    if index == len(subset):    # end of list, less then k num where picked, backtrack
        return

    subset[index] = True    # all sets that include this index
    subset_helper(subset, k, index + 1, picked + 1)

    subset[index] = False   # all sets that do not include this index
    subset_helper(subset, k, index + 1, picked)


def print_subset(subset):
    """
    :param subset: with k True values
    :return: prints out subset (idx of True values)
    """
    lst = []
    for idx, in_subset in enumerate(subset):
        if in_subset:
            lst.append(idx)
    print(lst)


# k_subset 2
def fill_k_subsets(n, k, lst):
    """
    :param n: set size
    :param k: subsets length
    :return: fill lst with all subsets
    """
    if k <= n:
        subset = [False] * n    # initializing list
        fill_helper(subset, k, 0, 0, lst)


def fill_helper(subset, k, index, picked, lst):
    """
    :param subset: list of current subset. True for chosen idx, else False.
    :param k:
    :param index: current idx
    :param picked: num of picked indices (num of True values in list) <= k
    :param lst: lst of subsets of length k
    :return: append all possible subsets to lst
    """
    if picked == k:     # k items where picked, append to lst
        lst_append_subset(subset, lst)

    if index < len(subset) and picked < k:
        subset[index] = True    # all sets that include this index
        fill_helper(subset, k, index + 1, picked + 1, lst)

        subset[index] = False   # all sets that do not include this index
        fill_helper(subset, k, index + 1, picked, lst)


def lst_append_subset(subset, lst):
    """
    :param subset: with k True values
    :param lst:
    :return: append subset to lst
    """
    sub_lst = []
    for idx, in_subset in enumerate(subset):
        if in_subset:
            sub_lst.append(idx)
    lst.append(sub_lst)


# k_subset 3
def return_k_subsets(n, k):
    """
    :param n: set size
    :param k: subsets length
    :return: list of lists (all possible k subset)
    """
    if k < 0 or n < k:
        return []
    if k == n:
        return [list(range(k))]
    return return_k_subsets(n-1, k) + [s + [n-1] for s in return_k_subsets(n-1, k-1)]

