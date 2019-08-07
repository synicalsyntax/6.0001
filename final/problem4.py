def longest_run(L):
    """
    Assumes L is a list of integers containing at least 2 elements.
    Finds the longest run of numbers in L, where the longest run can
    either be monotonically increasing or monotonically decreasing.
    In case of a tie for the longest run, choose the longest run
    that occurs first.
    Does not modify the list.
    Returns the sum of the longest run.
    """
    inc = []
    dec = []

    temp_inc = []
    temp_dec = []

    for i in range(1, len(L)):
        before = L[i - 1]
        current = L[i]

        if (len(temp_dec) > 1 and temp_dec[-1] < current):
            if (len(dec) < len(temp_dec)):
                dec = temp_dec.copy()
            temp_dec.clear()

        if (len(temp_inc) > 1 and temp_inc[-1] > current):
            if (len(inc) < len(temp_inc)):
                inc = temp_inc.copy()
            temp_inc.clear()

        if before == current:
            if (len(temp_inc) == 0):
                temp_inc = [before]
            if (len(temp_dec) == 0):
                temp_dec = [before]
            temp_inc.append(current)
            temp_dec.append(current)
        if before < current:
            if (len(temp_inc) == 0):
                temp_inc = [before]
            temp_inc.append(current)
        if before > current:
            if (len(temp_dec) == 0):
                temp_dec = [before]
            temp_dec.append(current)

        if (len(L) - 1 == i):
            if (len(dec) < len(temp_dec)):
                dec = temp_dec.copy()
            if (len(inc) < len(temp_inc)):
                inc = temp_inc.copy()

    run = []

    def stringify(array):
        return ' '.join([str(l) for l in array])

    if (len(dec) == len(inc)):
        string = stringify(L)
        inc_index = string.find(stringify(inc))
        dec_index = string.find(stringify(dec))
        run = inc.copy() if inc_index < dec_index else dec.copy()
    else:
        run = inc.copy() if len(inc) > len(dec) else dec.copy()
    return sum(run)
