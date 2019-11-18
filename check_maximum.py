# test function for the maximum function


from ex3 import maximum


def test():
    """contains list of tests for maximum function.
    returns if the func past the test"""
    test_0 = maximum([]), None
    test_1 = maximum([2, 2, 2]), 2
    test_2 = maximum([0, 3.0, 1]), 3.0
    test_3 = maximum([3.5, 5, 5]), 5
    tests = [test_0, test_1, test_2, test_3]

    return passed_test(tests)


def passed_test(tests):
    """for each test in list, checks if the func passed it.
    then, validate that all the tests status are success
    and returns a boolean expression"""

    passed_tests = 0
    for test_num, test in enumerate(tests):
        check, result = test
        if check == result:
            passed_tests += 1
            print("test " + str(test_num) + " SUCCESS")
        else:
            print("test " + str(test_num) + " FAIL")

    if passed_tests == len(tests):
        return True
    else:
        return False


if __name__ == '__main__':
    test()
