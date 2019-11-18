# test for find_pointers function in wordsearch file #

from wordsearch import find_pointers

IN_MATRIX = [['t', 'p', 'p', 'l', 'e'], ['c', 'g', 'o', 'a', 'o']]
NOT_IN_MATRIX = [['t', 'p', 'p', 'l', 'e'], ['c', 'g', 'o', 'V', 'o']]
ALL_SAME_MATRIX = [['a', 'a'], ['a', 'a']]
EMPTY_MATRIX = []
WORD = 'app'


def pointers_check():
    if find_pointers(IN_MATRIX, WORD) != [(1, 3)]:
        print('test 1 FAIL')
    if find_pointers(NOT_IN_MATRIX, WORD):  # if not an empty list
        print('test 2 FAIL')
    if find_pointers(ALL_SAME_MATRIX, WORD) != [(0, 0), (0, 1), (1, 0), (1, 1)]:
        print('test 3 FAIL')
    if find_pointers(EMPTY_MATRIX, WORD):   # if not an empty list
        print('test 4 FAIL')
    else:
        print('all tests SUCCESS')


if __name__ == '__main__':
    pointers_check()
