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

        if before <= current:
            if (len(temp_inc) == 0):
                temp_inc = [before]
            temp_inc.append(current)

        if before >= current:
            if (len(temp_dec) == 0):
                temp_dec = [before]
            temp_dec.append(current)

        if (len(L) - 1 == i):
            if (len(dec) < len(temp_dec)):
                dec = temp_dec.copy()
            if (len(inc) < len(temp_inc)):
                inc = temp_inc.copy()

    run = []

    def conjoin(int_list):
        """
        Conjoins an list of integers into a space-separated string.
        :param list: The list of integers to conjoin
        :type list: list of int
        :returns: A space-separated string of integers from the list.
        :rtype: str
        """
        return ' '.join([str(l) for l in int_list])

    if (len(dec) == len(inc)):
        string = conjoin(L)
        inc_index = string.find(conjoin(inc))
        dec_index = string.find(conjoin(dec))
        run = inc.copy() if inc_index < dec_index else dec.copy()
    else:
        run = inc.copy() if len(inc) > len(dec) else dec.copy()

    return sum(run)
