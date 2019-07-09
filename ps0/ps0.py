import numpy

x = int(input('Enter number x: '))
y = int(input('Enter number y: '))

exp = x ** y
log = numpy.log2(x)

print('X ** y = %d' % exp)
print('log(x) = %d' % log)
