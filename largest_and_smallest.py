# this function chooses the largest param and the smallest one out of three

def largest_and_smallest(n1,n2,n3):
    if n1 < n2 and n1 < n3:
        """n1 is the smallest"""
        small = n1
        if n2 < n3:
            large = n3
        else:
            large = n2
    elif n2 < n1 and n2 < n3:
        """n2 is the smallest """
        small = n2
        if n1 < n3:
            large = n3
        else:
            large = n1
    elif n3 < n1 and n3 < n2:
        """n3 is the smallest"""
        small = n3
        if n1 < n2:
            large = n2
        else:
            large = n1
    else:
        """2 numbers are equal and the smallest"""
        if n1 == n2 and n1 < n3:
            small = n1
            large = n3
        elif n1 == n3 and n1 < n2:
            small = n1
            large = n2
        elif n2 == n3 and n2 < n1:
            small = n2
            large = n1
        else:
            """all numbers are equal"""
            small = large = n1
    return large, small








