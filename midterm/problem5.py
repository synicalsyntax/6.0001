def dotProduct(listA, listB):
    '''
    listA: a list of numbers
    listB: a list of numbers of the same length as listA
    '''
    return sum([listA[i] * listB[i] for i in range(len(listA))])
