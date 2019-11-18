# this function checks the temperature for the last 3 days


def is_it_summer_yet(limit, day1, day2, day3):
    limit = int(limit)
    day1 = int(day1)
    day2 = int(day2)
    day3 = int(day3)

    if day1 > limit:
        if day2 > limit:
            """at least two are above limit"""
            return True
        elif day3 > limit:
            """at least two are above limit"""
            return True
        else:
            """only day1 is above limit"""
            return False

    elif day1 <= limit:
        if day2 > limit and day3 > limit:
            return True
        else:
            return False

