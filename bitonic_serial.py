from numpy import random, argmax
from sys import argv
from time import time

sol = []


def bitonic_sequence(a):
    a = list(random.randint(10000000000, size=(n)))
    a_ = a[1::2]
    a_.sort()
    a_.reverse()
    a = a[0::2]
    a.sort()
    a.extend(a_)
    return a


def bitonic_sort(a):
    if len(a) == 2:
        if a[0] > a[1]:
            a[0], a[1] = a[1], a[0]
        sol.append(a[0])
        sol.append(a[1])

        return
    
    n = int(len(a)/2)
    for i in range(n):
        if a[i] > a[n + i]:
            a[i], a[n + i] = a[n+ i], a[i]

    # print(a[n], a[-1])

    bitonic_sort(a[0: n])
    bitonic_sort(a[n:])


if __name__ == "__main__":
    # print(argv)
    n = int(argv[1])
    times = [1, n]
    n = int(2**n)
    time_bitonic_sequence = time()
    a = bitonic_sequence(n)
    time_bitonic_sequence = time() - time_bitonic_sequence
    times.append(time_bitonic_sequence)

    a_validate = list(a)
    a_validate.sort()
   
    time_bitonic_sort = time()
    bitonic_sort(a)
    a = sol
    time_bitonic_sort = time() - time_bitonic_sort
    times.append(time_bitonic_sort)
    
    if False not in [a == a_validate]:
        with open("bitonic_data.txt", 'a') as f:
            f.write(str(times))
            f.write("\n")
        print(times)
  
