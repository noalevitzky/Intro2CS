# several functions that uses while and for loops, as well as assert statement.


def input_list():
    """adding user inputs to a list"""
    lst = []
    user_input = input()
    while user_input:  # user_input is not a false object
        assert user_input != [], 'user input is an empty string'
        lst.append(user_input)
        user_input = input()
    return lst


def concat_list(str_list):
    """concat items from a given list and creates a new string"""
    str1 = ""
    assert isinstance(str_list, list), 'function parameter is not a list'
    for i, item in enumerate(str_list):         # item is a string
        assert isinstance(item, str), 'item in list is not a string'
        to_add = (' ' + item) if i else item
        str1 += to_add
    return str1


def maximum(num_list):
    """finding the list max num"""
    assert isinstance(num_list, list), "func param is not a list"
    if len(num_list) == 0:       # list is empty
        return None

    max_num = 0
    for num in num_list:
        assert num >= 0, "number is negative"
        if num > max_num:
            max_num = num
    return max_num


def cyclic(lst1, lst2):
    """checks if lst2 is a cyclic permutation of lst1"""
    assert isinstance(lst1, list)
    assert isinstance(lst2, list)
    if len(lst1) != len(lst2):
        return False
    if lst1 == [] and lst2 == []:
        return True

    perm_lst = find_permutation_cyclic(lst1, lst2)
    if perm_lst == []:
        return False
    else:
        return check_if_permutation_correct(perm_lst, lst1, lst2)


def find_permutation_cyclic(lst1, lst2):
    """finds if the first number in lst1 appears in lst2 and
     returns a suggested permutation"""
    permutation_lst = []
    for index, num_2 in enumerate(lst2):
        if lst1[0] == num_2:
            permutation = str(index % len(lst1))
            permutation_lst += permutation
    return permutation_lst


def check_if_permutation_correct(perm_lst, lst1, lst2):
    """checks if permutation is true for every suggested
     permutation in perm_lst"""
    index = 0
    len_lst = len(lst1)
    for permutation in perm_lst:
        permutation = int(permutation)
        while (lst1[index % len_lst] == lst2[(index + permutation) % len_lst]) \
                and (index != len_lst):
            index += 1
        if index == len_lst:
            return True
    return False


def seven_boom(num):
    """returns a list of the seven bom game callings"""
    assert isinstance(num, int)
    assert num > 0
    new_num = num + 1
    return boom_the_seven(new_num)


def boom_the_seven(num):
    """creating a list for the seven boom game, based on
     range of numbers including the given one"""
    seven_boom_lst = []
    for n in range(1, num):
        if n % 7 == 0:
            seven_boom_lst.append("boom")
        elif str(7) in str(n):
            seven_boom_lst.append("boom")
        else:
            seven_boom_lst.append(str(n))
    return seven_boom_lst


def histogram(n, num_list):
    """given the range size and list of numbers,
    returns the histogram"""
    assert isinstance(n, int)
    assert n > 0
    assert isinstance(num_list, list)
    return histogram_list(n, num_list)


def histogram_list(n, num_list):
    """counting how many times a number in given range
     appears in list, and creating the histogram"""
    histogram_lst = []
    for i, range_num in enumerate(range(n)):
        count_num = 0
        for j, num in enumerate(num_list):
            assert isinstance(num, int)
            assert num >= 0
            assert num < n
            if num == range_num:
                count_num += 1
        histogram_lst.append(count_num)
    return histogram_lst


def prime_factors(n):
    """given a number, returning the prime factor's list"""
    assert isinstance(n, int)
    assert n >= 1
    if n == 1:
        return []
    return prime_divider_list(n)


def prime_divider_list(n):
    """checks how many times each divider can divide the given
    number without modulo"""
    prime_factors = []
    for divider in range(2, n+1):
        while n % divider == 0:
            prime_factors.append(divider)
            n = n // divider
    return prime_factors


def cartesian(lst1, lst2):
    """given 2 lists, returns a list of the cartesian pairs"""
    if lst1 == [] or lst2 == []:
        return []
    return list_for_cartesian(lst1, lst2)


def list_for_cartesian(lst1, lst2):
    """creates the list of cartesian pairs"""
    cartesian_list = []
    for num1 in lst1:
        for num2 in lst2:
            pair = [num1, num2]
            cartesian_list.append(pair)
    return cartesian_list


def pairs(num_list, n):
    """finds the pairs that their sum is n"""
    assert isinstance(n, int)
    assert isinstance(num_list, list)
    if num_list == []:
        return []
    return list_of_pairs(num_list, n)


def list_of_pairs(num_list, n):
    """checks for any 2 nums in list if their sum equals
    n, and returns a list of all those pairs"""
    pairs_list = []
    for num1 in num_list:
        for num2 in num_list:
            assert isinstance(num1, int)
            assert isinstance(num2, int)
            if num1 != num2 and num1 + num2 == n and [num2, num1] not in pairs_list:
                pair = [num1, num2]
                pairs_list.append(pair)
    return pairs_list

