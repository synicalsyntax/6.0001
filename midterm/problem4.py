import math


def closest_power(base, num):
    '''
    base: base of the exponential, integer > 1
    num: number you want to be closest to, integer > 0
    Find the integer exponent such that base**exponent is closest to num.
    Note that the base**exponent may be either greater or smaller than num.
    In case of a tie, return the smaller value.
    Returns the exponent.
    '''
    result = math.log(num, base)
    floor = math.floor(result)
    ceil = math.ceil(result)

    def output(exponent):
        return abs(base ** exponent - num)

    if (output(floor) == output(ceil)):
        return floor

    return round(result)
