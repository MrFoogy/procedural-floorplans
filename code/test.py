import numpy

a = numpy.ndarray((2, 2), buffer=numpy.array([10,20,30,40]))
a.data = numpy.array([4,3,2,1])
for i in range(len(a)):
    print(i, a[i])
