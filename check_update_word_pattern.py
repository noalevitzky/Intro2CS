# tests the update_word_pattern function

from hangman import update_word_pattern


def test_update_pattern():
    input1 = ("coffee", "______", "f")
    pattern1 = "__ff__"
    input2 = ("tea", "___", "a")
    pattern2 = "__a"
    input3 = ("cookie", "coo_ie", "k")
    pattern3 = "cookie"
    input4 = ("zzzzzz", "______", "z")
    pattern4 = "zzzzzz"
    input_lst = [input1, input2, input3, input4]
    pattern_lst = [pattern1, pattern2, pattern3, pattern4]

    for test_input_index, test_input in enumerate(input_lst):
        word, pattern, letter = test_input
        if update_word_pattern(word, pattern, letter) != pattern_lst[test_input_index]:
            print("function \"update_word_pattern\" test FAIL")
            return False
    print("function \"update_word_pattern\" test SUCCESS")
    return True


if __name__ == '__main__':
    test_update_pattern()