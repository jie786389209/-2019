import numpy as np
import time

P = [[1, 7, 8, 9, 12,  6],
    [10, 2, 3, 4, 5, 11],
    [13, 14, 15, 16, 17, 18]]

starttime = time.clock()
P = [0 for i in range(1000)]
for i in range(10000):
    a = P[1]
endtime = (time.clock() - starttime)
print(endtime)
print(a)
starttime = time.clock()
P = np.zeros(1000)
for i in range(10000):
    a = P[1]
endtime = (time.clock() - starttime)
print(endtime)






# a = np.array([[0,1,1,1],
#              [0,1,0,1],
#               [1,1,1,0],
#               [0,1,0,1]])
#
# b = np.array([[0,1,1,1],
#              [0,1,0,1],
#               [1,1,1,0],
#               [0,1,0,1]])  + 1
#
# index = list(np.where(a[:,2] == 1)[0])
# a[index,:] = 2 * b[index, 1]
#
#
# print(list(np.where(a[:,2] == 1)[0]))
