trans = {'0': 'ling', '1': 'yi', '2': 'er', '3': 'san', '4': 'si',
         '5': 'wu', '6': 'liu', '7': 'qi', '8': 'ba', '9': 'jiu', '10': 'shi'}


def convert_to_mandarin(us_num):
    '''
    us_num, a string representing a US number 0 to 99
    returns the string mandarin representation of us_num
    '''
    if trans.get(us_num) is not None:
        return trans.get(us_num)
    if int(us_num) < 20:
        return ' '.join([trans['10'], trans[us_num[1:]]])
    if '0' in us_num:
        return ' '.join([trans[us_num[:1]], trans['10']])
    else:
        return ' shi '.join([trans[d] for d in us_num])
