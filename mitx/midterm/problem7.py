def dict_interdiff(d1, d2):
    '''
    d1, d2: dicts whose keys and values are integers
    Returns a tuple of dictionaries according to the instructions above
    '''
    dict_keys = set(d1.keys())
    for k in d2.keys():
        dict_keys.add(k)
    intersect = {}
    difference = {}
    for k in dict_keys:
        a = d1.get(k)
        b = d2.get(k)
        aPresent = a is not None
        bPresent = b is not None
        if (aPresent and bPresent):
            intersect[k] = f(a, b)
            continue
        if (aPresent):
            difference[k] = a
        if (bPresent):
            difference[k] = b
    return (intersect, difference)


# Sample f
def f(a, b):
    return a + b
