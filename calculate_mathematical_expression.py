# this function calculates math expressions between 2 numbers


def calculate_mathematical_expression(n1, n2, action):
    n1 = float(n1)
    n2 = float(n2)
    action = str(action)
    """calculates legal actions (not dividing by 0 or using illegal actions"""
    if action == "+":
        calc = n1 + n2
    elif action == "-":
        calc = n1 - n2
    elif action == "*":
        calc = n1 * n2
    elif action == "/":
        if n2 == 0:
            return None
        else:
            calc = n1 / n2
    else:
        return None

    return calc


# the following function converts a string to the needed params for the previous function


def calculate_from_string(text_message):
    """splits a string to the needed parameters for the previous calc"""
    text_message = str(text_message)
    param1, action, param2 = text_message.split(' ',maxsplit=3)
    action = str(action)
    param1 = float(param1)
    param2 = float(param2)
    return calculate_mathematical_expression(param1, param2, action)

