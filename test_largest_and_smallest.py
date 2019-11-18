# this function tests function 4 for 5 different cases


from largest_and_smallest import largest_and_smallest


def test_func_4():
    large, small = largest_and_smallest(-1, 1, 100)
    if large == 100 and small == -1:        # case 1 is true
        large, small = largest_and_smallest(100, 1, -1)

        if large == 100 and small == -1:        # case 2 is true
            large, small = largest_and_smallest(1, 100, -1)

            if large == 100 and small == -1:        # case 3 is true
                large, small = largest_and_smallest(0, 0, 0)

                if large == 0 and small == 0:       # case 4 is true
                    large, small = largest_and_smallest(0, 100, 0)

                    if large == 100 and small == 0:     # case 5 is true
                        print("Function 4 test success")
                        return True

                    else:       # case 5 is false
                        print("function 4 test fail")
                        return False

                else:       # case 4 is false
                    print("function 4 test fail")
                    return False

            else:       # case 3 is false
                print("function 4 test fail")
                return False

        else:       # case 2 is false
            print("function 4 test fail")
            return False

    else:       # case 1 is false
        print("function 4 test fail")
        return False


if __name__ == "__main__" :
    test_func_4()