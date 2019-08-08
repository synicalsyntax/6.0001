trans = {'0': 'ling', '1': 'yi', '2': 'er', '3': 'san', '4': 'si',
         '5': 'wu', '6': 'liu', '7': 'qi', '8': 'ba', '9': 'jiu', '10': 'shi'}


def convert_to_mandarin(us_num):
    '''
    us_num, a string representing a US number 0 to 99
    returns the string mandarin representation of us_num
    '''
    if trans.get(us_num) is not None:
        return trans.get(us_num)
    translations = [trans.get(num) for num in us_num]
    if int(us_num) < 20:
        return ' '.join([trans.get('10'), translations[1]])
    if '0' in us_num:
        return ' '.join([translations[0], trans.get('10')])
    else:
        return ' '.join([translations[0], trans.get('10'), translations[1]])
