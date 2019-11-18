###########################################################################
#   The following code executes the "hangman" game.                       #
#   The goal is to guess the chosen word by guessing letter by letter.    #
###########################################################################

import hangman_helper

MAX_ERRORS = hangman_helper.MAX_ERRORS
CHAR_A = 97


def create_pattern(word):
    """
    creating a pattern based on word length.
    """
    pattern = "_" * len(word)
    assert isinstance(pattern, str)
    return pattern


def update_word_pattern(word, pattern, letter):
    """
    the function gets 3 params- a word, the current pattern and a letter, and returns the updated pattern which
    includes the given letter.
    """
    assert isinstance(word, str)
    assert isinstance(pattern, str)
    assert isinstance(letter, str)
    pattern = update_pattern(word, pattern, letter)
    return pattern


def update_pattern(word, pattern, letter):
    """
    replaces underscores in the given pattern with the provided letter.
    """
    new_pattern = pattern
    for j, item in enumerate(word):
        if item == letter:
            new_pattern = new_pattern[:j] + letter + new_pattern[j + 1:]
    return new_pattern


def run_single_game(words_list):
    """
    gets a list of word and runs the game by steps.
    """
    # step1 - initializing
    error_count, msg, pattern, right_guess_lst, word, wrong_guess_lst = initializing_variables(words_list)

    # step2 - iteration
    while pattern != word and error_count < MAX_ERRORS:
        display_current(error_count, msg, pattern, wrong_guess_lst, ask_play=False)
        error_count, msg, pattern, wrong_guess_lst = game_iteration(error_count, msg, pattern, right_guess_lst, word,
                                                                    words_list, wrong_guess_lst)
    # step3 - end of game
    else:
        end_of_game(error_count, msg, pattern, word, wrong_guess_lst)


def end_of_game(error_count, msg, pattern, word, wrong_guess_lst):
    """
    sends a msg that the game is over and asks the user if he would like to play another game
    """
    msg = end_game_msg(pattern, word, error_count, msg)
    display_current(error_count, msg, pattern, wrong_guess_lst, ask_play=True)


def game_iteration(error_count, msg, pattern, right_guess_lst, word, words_list, wrong_guess_lst):
    """
    for every user action, a new iteration begins. this func checks if the user input is a letter or
    hint request and acts accordingly.
    """
    user_input_type, user_input = hangman_helper.get_input()
    if user_input_type == hangman_helper.LETTER:
        'input is a letter'
        pattern, error_count, wrong_guess_lst, msg, right_guess_lst = input_is_letter(error_count, pattern,
                                                                                      right_guess_lst, word,
                                                                                      wrong_guess_lst, user_input)
    elif user_input_type == hangman_helper.HINT:
        'input is a hint request'
        msg = input_is_hint(words_list, pattern, wrong_guess_lst, right_guess_lst)

    return error_count, msg, pattern, wrong_guess_lst


def initializing_variables(words_list):
    """
    initialize the game variables, based on words_list.
    """
    word = hangman_helper.get_random_word(words_list)
    wrong_guess_lst = []
    right_guess_lst = []
    error_count = 0
    pattern = create_pattern(word)
    msg = hangman_helper.DEFAULT_MSG
    return error_count, msg, pattern, right_guess_lst, word, wrong_guess_lst


def display_current(error_count, msg, pattern, wrong_guess_lst, ask_play):
    """
    present the current display.
    """
    hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg, ask_play)


def input_is_letter(error_count, pattern, right_guess_lst, word, wrong_guess_lst, user_input):
    """
    update variables based on user input (guess of a letter from the word).
    """
    letter = str(user_input)
    msg = hangman_helper.DEFAULT_MSG
    pattern, error_count, wrong_guess_lst, msg, right_guess_lst = update_variables(error_count, letter, msg, pattern,
                                                                                   word, wrong_guess_lst,
                                                                                   right_guess_lst)
    return pattern, error_count, wrong_guess_lst, msg, right_guess_lst


def input_is_hint(words_list, pattern, wrong_guess_lst, right_guess_lst):
    """
    returns the hint letter.
    """
    filtered_lst = filter_words_list(words_list, pattern, wrong_guess_lst, right_guess_lst)
    hint_letter = choose_letter(filtered_lst, pattern)
    msg = hangman_helper.HINT_MSG + hint_letter
    return msg


def update_variables(error_count, letter, msg, pattern, word, wrong_guess_lst, right_guess_lst):
    """
    when input is letter, the func displays current state, validate input, and update variables.
    """
    msg = validate_msg(letter, wrong_guess_lst, right_guess_lst, msg)
    if msg == hangman_helper.DEFAULT_MSG:  # user_input is valid
        if letter in word:
            if letter not in right_guess_lst:
                pattern = update_word_pattern(word, pattern, letter)
                right_guess_lst.append(letter)
        else:
            wrong_guess_lst.append(letter)
            error_count += 1
    return pattern, error_count, wrong_guess_lst, msg, right_guess_lst


def validate_msg(letter, wrong_guess_lst, right_guess_lst, msg):
    """
    checks if user_inout is a lowercase letter, that hasn't been guessed before.
    """
    lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
    if len(letter) == 1 and letter in lowercase_letters:
        if letter in wrong_guess_lst or letter in right_guess_lst:
            msg = hangman_helper.ALREADY_CHOSEN_MSG + letter
            return msg
        else:
            return msg
    else:
        msg = hangman_helper.NON_VALID_MSG
        return msg


def filter_words_list(words, pattern, wrong_guess_lst, right_guess_lst):
    """
    returns a list of words that matches the stated conditions out of words list.
    """
    filtered_lst = []
    for checked_word in words:
        if len(checked_word) == len(pattern):
            if compare_checked_to_pattern(checked_word, pattern, right_guess_lst):
                if compare_checked_to_wrong_guess_lst(checked_word, wrong_guess_lst):
                    filtered_lst.append(checked_word)
    return filtered_lst


def compare_checked_to_wrong_guess_lst(checked_word, wrong_guess_lst):
    """
    validate that the checked word doesn't contain letters from the wrong_guess_lst.
    """
    for letter in checked_word:
        if letter in wrong_guess_lst:
            return False
        else:
            return True


def compare_checked_to_pattern(checked_word, pattern, right_guess_lst):
    """
    validate that all the guessed letters appear in the checked word in the same index, and not in any other index.
    """
    for p, pattern_letter in enumerate(pattern):
        if pattern_letter != "_" and pattern_letter != checked_word[p]:
            return False
        elif pattern_letter == "_" and checked_word[p] in right_guess_lst:
            return False
    return True


def choose_letter(words, pattern):
    """
    returns the most common letter in words lst.
    """
    letters_lst = [0] * 26
    for word in words:
        for letter in word:
            if letter not in pattern:
                letter_index = ord(letter.lower()) - CHAR_A
                letters_lst[letter_index] += 1
    count_hint = max(letters_lst)
    index_hint = letters_lst.index(count_hint)
    hint_letter = chr(index_hint + CHAR_A)
    return hint_letter


def random_word(words_list):
    """
    choose a random word from list, and define several variables.
    """
    word = hangman_helper.get_random_word(words_list)
    assert isinstance(word, str)
    return word


def end_game_msg(pattern, word, error_count, msg):
    """
    returns a msg which specifies the reason of the game ending.
    """
    if pattern == word:
        msg = hangman_helper.WIN_MSG
    elif error_count == MAX_ERRORS:
        msg = hangman_helper.LOSS_MSG + word
    return msg


def main():
    """
    responsible of the running of the game.
    """
    a = True
    words_lst = hangman_helper.load_words()

    while a:
        run_single_game(words_lst)
        user_input_type, user_input = hangman_helper.get_input()
        if user_input_type == hangman_helper.PLAY_AGAIN:
            'input is either true (user wants to play another game) or false'
            if not user_input:
                a = False


if __name__ == '__main__':
    hangman_helper.start_gui_and_call_main(main)
    hangman_helper.close_gui()
