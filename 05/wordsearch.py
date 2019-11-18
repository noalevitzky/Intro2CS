#  this program executes the word search game  #
#       based on args in command line          #

import sys
import os

ARGS = sys.argv
WORD_FILE_INDEX = 1
MATRIX_FILE_INDEX = 2
OUTPUT_FILE_INDEX = 3
DIRECTIONS_INDEX = 4
IDEAL_ARGS_LEN = 5


def check_input_args(args):
    """
    checks that the args are valid.
    if not valid, returns an error msg. if valid, returns None.
    """
    msg = None
    valid_directions = 'udrlwxyz'
    missing_arg_msg = 'There are missing arguments in the commend line'
    missing_wordfile_msg = 'The word file is missing'
    missing_matrix_msg = 'The matrix file is missing'
    illegal_direction_msg = 'Illegal direction/s'
    # validate input
    if len(args) != IDEAL_ARGS_LEN:
        msg = missing_arg_msg
    else:
        if not os.path.exists(args[MATRIX_FILE_INDEX]):
            msg = missing_matrix_msg
        elif not os.path.exists(args[WORD_FILE_INDEX]):
            msg = missing_wordfile_msg
        for char in args[DIRECTIONS_INDEX]:
            if char not in valid_directions:
                msg = illegal_direction_msg
    return msg


def read_wordlist_file(filename):
    """
    opens the file, reads the words inside
    and returns a list of those words
    """
    with open(filename) as f:
        word_list = f.read().splitlines()
        f.close()
    return word_list


def read_matrix_file(filename):
    """
    opens the file, reads the matrix, and returns a
    two-dimensional list of the matrix letters
    """
    mat_list = []
    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            line = line.rsplit(',')
            mat_list.append(line)
            f.close()
    return mat_list


def find_words_in_matrix(word_list, matrix, directions):
    """
    searches each word from word_list in matrix, according
    to the given search directions. the function counts
    each word's appearances and saves it.
    the func returns a list of pairs (tuple)- (word, count)
    where word is of type str and count is int.
    """
    count_dictionary = create_count_dictionary(word_list)
    for word in word_list:
        pointers_list = find_pointers(matrix, word)
        for pointer in pointers_list:
            if 'd' in directions and d_search(matrix, word, pointer):
                count_dictionary[word] += 1
            if 'u' in directions and u_search(matrix, word, pointer):
                count_dictionary[word] += 1
            if 'r' in directions and r_search(matrix, word, pointer):
                count_dictionary[word] += 1
            if 'l' in directions and l_search(matrix, word, pointer):
                count_dictionary[word] += 1
            if 'w' in directions and w_search(matrix, word, pointer):
                count_dictionary[word] += 1
            if 'x' in directions and x_search(matrix, word, pointer):
                count_dictionary[word] += 1
            if 'y' in directions and y_search(matrix, word, pointer):
                count_dictionary[word] += 1
            if 'z' in directions and z_search(matrix, word, pointer):
                count_dictionary[word] += 1
    return dictionary_to_list(count_dictionary)


def dictionary_to_list(count_dictionary):
    """
    transform the count dictionary to a list, while
    removing words that do not appear in matrix
    """
    word_count_list = []
    for (word, count) in count_dictionary.items():
        if count != 0:
            word_count_list.append((word, count))
    return word_count_list


def create_count_dictionary(word_list):
    """
    creates a count dictionary where the keys are words
    in wordlist, and initialize the count (= 0)
    """
    count_dictionary = {}
    for word in word_list:
        count_dictionary[word] = 0
    return count_dictionary


def find_pointers(matrix, word):
    """
    finds the index pairs (row,column) in matrix,
    where the first letter in word appears.
    """
    pointers_list = []
    for row_index, row in enumerate(matrix):
        for mat_char_index, mat_char in enumerate(matrix[row_index]):
            if word[0] == mat_char:
                char_pair = (row_index, mat_char_index)
                pointers_list.append(char_pair)
    return pointers_list


def d_search(matrix, word, pointer):
    """
    checks if the given word appears in matrix,
    given a pointer (location of first char in word)
    and a direction (down)
    """
    i, j = pointer
    num_rows = len(matrix)
    if num_rows - i < len(word):
        return False
    for k in range(len(word)):
        row = matrix[i+k]
        char = word[k]
        if row[j] != char:
            return False
    return True


def u_search(matrix, word, pointer):
    """
    checks if the given word appears in matrix,
    given a pointer (location of first char in word)
    and a direction (up)
    """
    i, j = pointer
    if i + 1 < len(word):
        return False
    for k in range(len(word)):
        row = matrix[i-k]
        char = word[k]
        if row[j] != char:
            return False
    return True


def r_search(matrix, word, pointer):
    """
    checks if the given word appears in matrix,
    given a pointer (location of first char in word)
    and a direction (right)
    """
    i, j = pointer
    num_columns = len(matrix[0])
    if num_columns - j < len(word):
        return False
    for k in range(len(word)):
        row = matrix[i]
        char = word[k]
        if row[j+k] != char:
            return False
    return True


def l_search(matrix, word, pointer):
    """
    checks if the given word appears in matrix,
    given a pointer (location of first char in word)
    and a direction (left)
    """
    i, j = pointer
    num_columns = len(matrix[0])
    if num_columns + 1 < len(word):
        return False
    for k in range(len(word)):
        row = matrix[i]
        char = word[k]
        if row[j-k] != char:
            return False
    return True


def w_search(matrix, word, pointer):
    """
    checks if the given word appears in matrix,
    given a pointer (location of first char in word)
    and a direction (up-right diagonal)
    """
    i, j = pointer
    num_columns = len(matrix[0])
    if num_columns - j < len(word) or i + 1 < len(word):
        return False
    for k in range(len(word)):
        row = matrix[i - k]
        char = word[k]
        if row[j + k] != char:
            return False
    return True


def x_search(matrix, word, pointer):
    """
    checks if the given word appears in matrix,
    given a pointer (location of first char in word)
    and a direction (up-left diagonal)
    """
    i, j = pointer
    num_columns = len(matrix[0])
    if num_columns + 1 < len(word) or i + 1 < len(word):
        return False
    for k in range(len(word)):
        row = matrix[i - k]
        char = word[k]
        if row[j - k] != char:
            return False
    return True


def y_search(matrix, word, pointer):
    """
    checks if the given word appears in matrix,
    given a pointer (location of first char in word)
    and a direction (down-right diagonal)
    """
    i, j = pointer
    num_columns = len(matrix[0])
    num_rows = len(matrix)
    if num_columns - j < len(word) or num_rows - i < len(word):
        return False
    for k in range(len(word)):
        row = matrix[i + k]
        char = word[k]
        if row[j+k] != char:
            return False
    return True


def z_search(matrix, word, pointer):
    """
    checks if the given word appears in matrix,
    given a pointer (location of first char in word)
    and a direction (down-left diagonal)
    """
    i, j = pointer
    num_columns = len(matrix[0])
    num_rows = len(matrix)
    if num_columns + 1 < len(word) or num_rows - i < len(word):
        return False
    for k in range(len(word)):
        row = matrix[i+k]
        char = word[k]
        if row[j-k] != char:
            return False
    return True


def write_output_file(results, output_filename):
    """
    creates/ override a file named after the param,
    and writes the outputs in it
    """
    results_list = create_results_list(results)
    with open(output_filename, 'w') as f:
        f.write('\n'.join(results_list))
        f.close()


def create_results_list(results):
    """
    converts results (a list of tuples, where items
    in tuples are str/int) to a list of strings.
    """
    tuple_list = []
    string_list = []
    for (word, count) in results:
        tuple_list.append((word, str(count)))
    for item in tuple_list:
        string_list.append(','.join(item))
    return string_list


def run_game():
    """
    given the args in the command line, this function is
    executing the program, and returning and output of the
    found words in an output file (same folder as the args files).
    """
    msg = check_input_args(ARGS)
    if msg:     # args are not valid, error msg
        print(msg)
    else:
        word_list = read_wordlist_file(ARGS[WORD_FILE_INDEX])       # creates the wordlist
        if not word_list:
            write_output_file([], 'matrix_output_file.txt')
        else:
            matrix = read_matrix_file(ARGS[MATRIX_FILE_INDEX])  # creates the matrix
            directions = ARGS[DIRECTIONS_INDEX]
            word_count_list = find_words_in_matrix(word_list, matrix, directions)     # find words in matrix
            write_output_file(word_count_list, 'matrix_output_file.txt')    # create output file with found words


if __name__ == '__main__':
    run_game()
