def flatten(aList):
    '''
    aList: a list
    Returns a copy of aList, which is a flattened version of aList
    '''
    flat = []
    for e in aList:
        if (isinstance(e, list)):
            flat.extend(flatten(e))
        else:
            flat.append(e)
    return flat
