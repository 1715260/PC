from mpi4py import MPI
from numpy import random, argmax, array, empty, concatenate
from math import log
from sys import argv
from time import time


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
sol = []
def bitonic_sequence(n, n_):
    if size > 1:
	# Create a bitonic sequence
        if rank == 0:
            a = list(random.randint(10000000000, size=(n)))
            a_ = a[1::2]
            a = array(a[0::2])
            comm.Send([a, MPI.INT], dest=1, tag=0)
            a_.sort()
            a_.reverse()
            a = empty(shape=(n_), dtype=int)
            req = comm.Irecv([a, MPI.INT], source=1, tag=1)
            req.wait()
            a = list(a)
            a.extend(a_)

            return array(a)

        if rank == 1:
            a = empty(shape=(n_), dtype=int)
            comm.Recv([a, MPI.INT], source=0, tag=0)
            a.sort()

            req = comm.Isend([a, MPI.INT], dest=0, tag=1)
            req.wait()
        

def bitonic_sort_serial(a):
    if len(a) == 2:
        if a[0] > a[1]:
            a[0], a[1] = a[1], a[0]
        sol.append(a[0])
        sol.append(a[1])

        return

    n = int(len(a)/2)
    for i in range(n):
        if a[i] > a[n + i]:
            a[i], a[n + i] = a[n + i], a[i]

    bitonic_sort_serial(a[0: n])
    bitonic_sort_serial(a[n:])

def bitonic_sort(a, np=int(log(size, 2))):
    if np > 0:
        processors = [i for i in range(0, size, int(2**np))]
        next = [i for i in range(0, size, int(2**(np-1)))]

        
        if rank in processors:
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

            comm.isend(n, dest=rank + np, tag=46)
            comm.Isend([a[n:], MPI.INT], dest=rank+np, tag=47)
            bitonic_sort(a[0: n], np=np-1)

        elif rank in next and rank not in processors:
            
            req = comm.irecv(source=rank-np, tag=46)
            n = req.wait()
            a = empty(shape=n, dtype=int)
            req = comm.Irecv([a, MPI.INT], source=rank -np, tag=47)
            req.wait()
            bitonic_sort(a, np=np-1)
        
        else:
            bitonic_sort(a, np=np-1)

    else:
        return bitonic_sort_serial(a)

def merge(a, np=1):
    np_ = int(2**np)
    diff = int(np_/2)
    if np_ <= size:
        processor = [i for i in range(0, size, np_)]
        sender = [i + diff for i in processor]
        if rank in sender:
            req = comm.Isend([a, MPI.INT], dest=rank-diff, tag=33)
        
        elif rank in processor:
            a_ = empty(shape=a.shape[0], dtype=int)
            req = comm.Irecv([a_, MPI.INT], rank + diff, tag=33)
            req.wait()
            a = list(a)
            a_ = list(a_)
            a.extend(a_)
            return merge(array(a), np=np+1)
    return a


if __name__ == "__main__":
    a = []
    times = []
    if rank == 0 or rank == 1:
        n = int(argv[1])
        times.append(size)
        times.append(n)
        n = int(2**n)
        n_ = int(n/2)
        time_bitonic_sequence = time()
        a = bitonic_sequence(n, n_)
        time_bitonic_sequence = time() - time_bitonic_sequence
    
        if rank == 0:
            a_validate = list(a)
            a_validate.sort()
            times.append(time_bitonic_sequence)
    time_bitonic_sort = time()
    bitonic_sort(a)
    sol = array(sol)
    
    
    if rank == 0:
        a = merge(sol)
        time_bitonic_sort = time() - time_bitonic_sort
        times.append(time_bitonic_sort)
        if False not in [list(a) == a_validate]:
            with open("bitonic_data.txt", 'a') as f:
                f.write(str(times))
                f.write("\n")
            print(times)
        
    else:
        merge(sol)
 
