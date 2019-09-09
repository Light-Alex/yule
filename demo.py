import uuid
import numpy as np

# a = 'http://www.ylq.com/oumei/madiyesilaoruisen/'
# b = a.split('/')
# print(b)
# print(int(uuid.uuid1()))
# n = 0
# a = int(uuid.uuid1())
# while a:
#     n += 1
#     a = a // 10
# print(n)

# a = np.array([1, 2, 3])
# b = np.array([2, 3, 4])
# print(a)
# print(b)
#
# a1 = np.stack((a, b), axis=0)
# print(a1)
# b1 = np.stack((a, b), axis=1)
# print(b1)

n_label = 2
a = np.random.uniform(-1, 1, n_label).astype('f')
b = np.random.uniform(-1, 1, n_label).astype('f')
print('a:', a)
print('b:', b)
x1 = np.stack([b, a])
x2 = np.stack([a])
print('x1:', x1)
print('x2:', x2)
xs = [x1, x2]
print(xs)


