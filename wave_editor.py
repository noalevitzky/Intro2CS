# The following code is an editing audio program, of files type wav.


import math
from wave_helper import *


GLOBAL_SAMPLE_RATE = 2000
FREQ_DICT = {'A': 440, 'B': 494, 'C': 523, 'D': 587, 'E': 659, 'F': 698, 'G': 784, 'Q': 0}
MAX_VOLUME = 32767
PI = math.pi
TIME_SAMPLES_RATIO = 125
VOLUME_MULITPLICATION = 1.2


############################################################
#                    change wav functions                  #
############################################################


def change_wav_menu(existing_frame_rate=GLOBAL_SAMPLE_RATE, existing_audio_data=False):
    if not existing_audio_data:  # audio data do not exist, first time user is here
        valid = False
        while not valid:
            file_name = input('A change is coming, I can feel it!\n'
                              'Please enter the wav file name: ')
            if load_wave(file_name) == -1:
                print('Damn it. file is invalid\n*****************************')
            else:  # file is valid
                frame_rate, audio_data = load_wave(file_name)
                valid = True
    elif existing_audio_data:
        # audio data already exists, user was directed here from a change function
        audio_data = existing_audio_data
        frame_rate = existing_frame_rate
    reverse = '1'
    speed_up = '2'
    slow_down = '3'
    higher = '4'
    lower = '5'
    low_pass = '6'
    option = False
    while not option:
        user_input = input('We all need a change once in a while.\n'
                           'Please select one of the following options-\n'
                           '(1= reverse, 2= speed up, 3= slow down, 4= volume up, 5= volume down,'
                           '6= low pass filter): ')
        if user_input in ('1', '2', '3', '4', '5', '6'):
            option = user_input
        else:       # input is invalid
            print('Oh no! Your input is invalid!\n*****************************')
    if option == reverse:
        changed_audio_data = reverse_wav(audio_data)
    elif option == speed_up:
        changed_audio_data = speed_up_wav(audio_data)
    elif option == slow_down:
        changed_audio_data = slow_down_wav(audio_data)
    elif option == higher:
        changed_audio_data = higher_sound(audio_data)
    elif option == lower:
        changed_audio_data = lower_sound(audio_data)
    elif option == low_pass:
        changed_audio_data = low_pass_filter(audio_data)
    transition_menu(frame_rate, changed_audio_data)


def reverse_wav(lst):
    """
    reverse a given list and return it.
    """
    lst.reverse()
    return lst


def speed_up_wav(lst):
    """
    return a new list that contains only partial values from given list.
    (having less samples in wav list == speeding up the wav sound).
    the values' selection is based on the SPEED magic number.
    """
    boosted_list = []
    for idx, sample in enumerate(lst):
        if idx % 2 == 0:    # only even
            boosted_list.append(sample)
    return boosted_list


def slow_down_wav(lst):
    """
    return a new list with added avg values.
    (having more samples in wav list == slowing down the wav sound).
    the avg is of every 2 adjacent values in list.
    """
    slowed_list = []
    prev_sample = None
    for idx, sample in enumerate(lst):
        if prev_sample:
            avg_sample = calc_avg_samples(prev_sample, sample)
            slowed_list.append(avg_sample)
        slowed_list.append(sample)
        prev_sample = sample
    return slowed_list


def calc_avg_samples(sample1, sample2, sample3=False):
    """
    calculate the avg of given values.
    could except up to 3 values.
    """
    i1, j1 = sample1
    i2, j2 = sample2
    if sample3:     # sample3 exists
        i3, j3 = sample3
        avg_sample = [int((i1 + i2 + i3)/3), int((j1 + j2 + j3)/3)]
    else:   # only 2 samples where given
        avg_sample = [int((i1 + i2)/2), int((j1 + j2)/2)]
    return avg_sample


def low_pass_filter(lst):
    """
    return a low_pass_list list, which is created by replacing every value in
    given list with an avg one. first value of new list is an avg of first
    and second values in given list. last value of new list is an avg of last
    value of given list and the one to its left. any other value of new list
     is an avg of three values in given list (value from given list in the
    same index of the new, and its adjacent values)
    """
    low_pass_list = []
    prev2prev_value = None
    prev_value = lst[0]
    avg_sample = None
    for idx, value in enumerate(lst):
        if idx < len(lst)-1:   # not last value of given list
            if idx == 0:
                continue
            if idx == 1:    # calc first value of low_pass_list
                avg_sample = calc_avg_samples(prev_value, value)
            elif idx > 1:   # calc second till second2last values of low_pass_list
                avg_sample = calc_avg_samples(prev2prev_value, prev_value, value)
            low_pass_list.append(avg_sample)
            prev2prev_value = prev_value
            prev_value = value
        else:       # calc second2last & last values of low_pass_list
            avg_sample1 = calc_avg_samples(prev2prev_value, prev_value, value)
            avg_sample2 = calc_avg_samples(prev_value, value)
            low_pass_list.extend([avg_sample1, avg_sample2])
    return low_pass_list


def volume_out_of_range(wav_list_left_right):
    """
    this function checks whether the the volume in the wav list
    frame is abbove maximum or below minimum. if so, it changes the volume to
    the maximum volume/minimum
    :param wav_list_left_right: 1 frame from the wav list
    :return: the frame after checking
    """
    if wav_list_left_right[0] > 32767 or wav_list_left_right[0] < -32768:
        if wav_list_left_right[0] < 0:
            wav_list_left_right[0] = -32768
        else:
            wav_list_left_right[0] = 32767
    if wav_list_left_right[1] > 32767 or wav_list_left_right[1] < -32768:
        if wav_list_left_right[1] < 0:
            wav_list_left_right[1] = -32768
        else:
            wav_list_left_right[1] = 32767
    return wav_list_left_right


def higher_sound(wav_list):
    """
    this function takes all the wave list, and maximizes each frame times 1.2
    :param wav_list:
    """
    for index_wav_list in range(len(wav_list)):
        wav_list[index_wav_list][0] = \
            int(wav_list[index_wav_list][0] * VOLUME_MULITPLICATION)
        wav_list[index_wav_list][1] = \
            int(wav_list[index_wav_list][1] * VOLUME_MULITPLICATION)
        wav_list[index_wav_list] = volume_out_of_range(wav_list[index_wav_list])
    return wav_list


def lower_sound(wav_list):
    """
    this function takes all the wave list, and minimizes each frame by dividing
     it by 1.2
    :param wav_list:
    """
    for index_wav_list in range(len(wav_list)):
        wav_list[index_wav_list][0] = \
            int(wav_list[index_wav_list][0] / VOLUME_MULITPLICATION)
        wav_list[index_wav_list][1] = \
            int(wav_list[index_wav_list][1] / VOLUME_MULITPLICATION)
        wav_list[index_wav_list] = volume_out_of_range(wav_list[index_wav_list])
    return wav_list


############################################################
#                          merging                         #
############################################################


def wav_list_merge_for_equal_frame_rates(wav_lst1, wav_lst2):
    """
    this function get two unequal length wave lists, and merges them to
    one new wav_list, by averaging them. once the bigger list ends,
    it just adds the leftover frames from the bigger list
    :return: new merged wav list
    """
    new_wav_lst = []
    for index_length in range(max(len(wav_lst1), len(wav_lst2))):
        try:
            new_wav_lst.append(calc_avg_samples(wav_lst1[index_length], wav_lst2[index_length]))
        except IndexError:
            try:
                new_wav_lst.append(wav_lst1[index_length])
            except IndexError:
                try:
                    new_wav_lst.append(wav_lst2[index_length])
                except IndexError:
                    return new_wav_lst
    return new_wav_lst


def euclid_gcd(x, y):
    while y > 0:
        x, y = y, x % y
    return x


def collision_unequal_frame_rate(slower_wav_list, slower_magic_number, faster_wav_list, faster_magic_number):
    """
    this funciton gets as an input two unequal (by frame rate) wave lists.
    it averages every matching item in each list, (calculated by the gc).
    if the faster list ends before the slower - the new wav_list returned
    will be added the remaining items as they are from the slow list.
    if the slower list ends before the fast - ww will add the remaining
    items in the faster list by the same method (with the gc) untill we
    finish going over the list
    :param slower_magic_number: slower frame rate devided by the maximal number
    that devides both the original frame rate 1 and the original frame rate 2
    :param faster_magic_number: faster frame rate devided by the maximal number
    that devides both the original frame rate 1 and the original frame rate 2
    :return:
    """
    new_wav_lst = slower_wav_list
    index_slower_wav_list = 0
    index_faster_wav_list = 0
    while index_slower_wav_list in range(len(slower_wav_list)):
        try:
            if (index_faster_wav_list % faster_magic_number) < slower_magic_number:
                new_wav_lst[index_slower_wav_list] = \
                    (calc_avg_samples(slower_wav_list[index_slower_wav_list],
                                      faster_wav_list[index_faster_wav_list]))
                index_faster_wav_list += 1
                index_slower_wav_list += 1
            else:
                index_faster_wav_list = \
                    int(index_faster_wav_list + faster_magic_number - slower_magic_number)
        except IndexError:
            return new_wav_lst
    if index_faster_wav_list < len(faster_wav_list):
        while index_faster_wav_list in range(len(faster_wav_list)):
            if index_faster_wav_list % faster_magic_number < slower_magic_number:
                new_wav_lst.append(faster_wav_list[index_faster_wav_list])
                index_faster_wav_list += 1
            else:
                index_faster_wav_list = \
                    int(index_faster_wav_list + faster_magic_number - slower_magic_number)
    return new_wav_lst


def wav_list_collision(wav_lst1, frame_rate1, wav_lst2, frame_rate2):
    """
    start of work on merging two wav lists. the first scenario is for an equal
    frame rate two list - in this case we will just merge by average each
    frame from each list.
    if the
    :param wav_lst1:
    :param frame_rate1:
    :param wav_lst2:
    :param frame_rate2:
    """
    if frame_rate1 == frame_rate2:
        return wav_list_merge_for_equal_frame_rates(wav_lst1, wav_lst2), frame_rate2
    else:
        # frame rates unequal
        new_frame_rate = min(frame_rate2, frame_rate1)
        gc = euclid_gcd(max(frame_rate1, frame_rate2), min(frame_rate1, frame_rate2))
        wav_lst1_magic_number = frame_rate1 / gc
        wav_lst2_magic_number = frame_rate2 / gc
        if frame_rate1 < frame_rate2:
            new_wav_lst = collision_unequal_frame_rate \
                (wav_lst1, wav_lst1_magic_number, \
                 wav_lst2, wav_lst2_magic_number)
        else:
            # frame rate 2 is faster
            new_wav_lst = collision_unequal_frame_rate \
                (wav_lst2, wav_lst2_magic_number, \
                 wav_lst1, wav_lst1_magic_number)
    return new_wav_lst, new_frame_rate


def check_input(input_files):
    """
    this function checks if the input by the user is valid.
    if it is constructed of 2 files, and if the load file function
    will return us an error, this function will raise a flag early
    :return: message if not valid, and False. if valid - just an empty string
    True
    """
    message = ''
    input_files = input_files.split(' ')
    if len(input_files) != 2:
        message = 'You did not put 2 files in your input!\n******'
        return message, False
    elif load_wave(input_files[0]) == -1 or load_wave(input_files[1]) == -1:
        message = 'something is wrong with the files. please try again\n*******'
        return message, False
    else:
        return message, True


def menu_for_collision():
    """
    this function is the menu for merging 2 wave lists. it asks the user for
    two files, checks validity, creates two frame rates and 2 wave lists out
    of them. and then creates a merged wave list, and frame rate, out of them.
    :return: in the end the function just calls the transition menu, while
    sending to it the new wav list and the new frame rate.
    """
    string_of_files = input('Two are better than one!\n'
                            'Please insert 2 files to merge in the following format: <file1_path> <file2_path>')
    message, valid_input = check_input(string_of_files)
    while valid_input is not True:
        print(message)
        string_of_files = input('please try again')
        message, valid_input = check_input(string_of_files)
    string_of_files = string_of_files.split(' ')
    frame_rate1, wav_lst1 = load_wave(string_of_files[0])
    frame_rate2, wav_lst2 = load_wave(string_of_files[1])
    new_wav_lst, new_frame_rate = \
            wav_list_collision(wav_lst1, frame_rate1, wav_lst2, frame_rate2)
    transition_menu(new_frame_rate, new_wav_lst)


############################################################
#                     music composing                      #
############################################################


def music_composing():
    """
    return a list with the composed music, based on a valid instruction file.
    then, leads to the transition menu.
    """
    lst = []
    notes_list = []
    valid = False
    while not valid:
        file_name = input('Dear Beethoven,\n'
                          'enter your amazing instructions file name: ')
        notes_list = instructions_list(file_name)
        if not file_validation(notes_list):
            print('Instructions are invalid (we probably should have asked Mozart...)\n'
                  'Either the file is empty, or char is not valid\n***************')
        else:
            valid = True
    for k in range(0, len(notes_list), 2):  # range of even indices (k = note)
        note = str(notes_list[k])
        time = int(notes_list[k+1])
        num_samples = time_to_num_samples(time)
        j = (0, 0)  # Q (0,0) before a new note
        lst.append(j)
        for i in range(1, num_samples):
            sample_tuple = calculate_sample(note, i)
            lst.append(sample_tuple)
    transition_menu(GLOBAL_SAMPLE_RATE, lst)


def time_to_num_samples(time):
    """
    return samples num based on given note time
    """
    num_samples = time * TIME_SAMPLES_RATIO
    return num_samples


def calculate_sample(note, i):
    """
    calculate the sample rate based on given note and sample index i.
    """
    if FREQ_DICT[note] == 0:    # if note = Q
        sample_tuple = (0, 0)
    else:
        sample_per_cycle = GLOBAL_SAMPLE_RATE / FREQ_DICT[note]
        sin = math.sin(PI*2*(i/sample_per_cycle))
        sample = int(MAX_VOLUME * sin)
        sample_tuple = (sample, sample)
    return sample_tuple


def instructions_list(file_name):
    """
    extract instruction list out of file
    """
    with open(file_name, 'r') as f:
        lst = f.read().rsplit()
        f.close()
    return lst


def file_validation(note_list):
    """
    check if note list is valid:
    list should not be empty, every char should be either
    a valid note (as specified in dict) or an int.
    """
    if not note_list:  # file is empty, thus list too
        return False
    for char in note_list:
        if char not in FREQ_DICT and not char.isdigit():    # invalid note
            return False
        elif '.' in char:     # time is not of type int
            return False
    else:
        return True


############################################################
#                     transition menu                      #
############################################################


def transition_menu(frame_rate, wave_list):
    """
    direct user to either save his changes or continue editing the audio file
    """
    save = '1'
    change = '2'
    option = False
    while not option:
        user_input = input('Transitions themselves are not the issue,\n'
                           'but how well you respond to their challenges!\n'
                           'Please choose one of the following challenges-\n'
                           '(1= save wav, 2= change wav): ')
        if user_input == save or user_input == change:
            option = user_input
        else:       # input is invalid
            print('Oh no! Your input is invalid!\n*****************************')
            option = False
    if option == save:
        save_file(frame_rate, wave_list)
    elif option == change:
        change_wav_menu(frame_rate, wave_list)    # file exists


def save_file(frame_rate, wav_lst):
    """
    this function gets the wav list and the frame rate, asks the user for a
    file name, and saves the new audio file
    :param frame_rate: of the new file to save
    :param wav_lst: of the new file to save
    """
    file_name = input('You could save the world!\n'
                      'But for now, just enter a file name, '
                      'in which you want to save your changes: ')
    save_wave(frame_rate, wav_lst, file_name)
    main_menu()


def main_menu():
    """
    the main menu of the program, asks the user what to do and leads to
    the relevant function
    """
    change = '1'
    merge = '2'
    composing = '3'
    exit_program = '4'
    option = False
    while not option:
        user_input = input('Hello there, protector of the universe!\n'
                           'please choose one of the following options-\n'
                           '(1= change wave ,2= merge 2 wav file, 3= compose a new wav file, 4= exit): ')
        if user_input == change or user_input == merge or \
                user_input == composing or user_input == exit_program:
            option = user_input
        else:  # input is invalid
            print('Your input is invalid!\nbetter luck next time!\n*****************************')
            option = False
    if option == change:
        change_wav_menu()
    elif option == merge:
        menu_for_collision()
    elif option == composing:
        music_composing()
    else:
        print('Farewell my friend, it was a pleasure!')


if __name__ == '__main__':
    main_menu()