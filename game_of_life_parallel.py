# TODO check send vs Send


from mpi4py import MPI
from numpy import array, zeros, empty
from sys import argv

def merge(alive1, alive2, grid):
    pass


def alive(n, m, grid):
    alive = zeros(shape=(n,m))
    starti, startj = -1, -1
    endi, endj = 2, 2
    for i in range(0, n):
        for j in range(0, m):
            alive_ = 0
            alive_ -= grid[i][j]
            if i == 0:
                starti = 0
            else:
                starti = -1

            if j == 0:
                startj = 0
            else:
                startj = -1

            if i == n - 1:
                endi = 1
            else:
                endi = 2
            
            if j == m - 1:
                endj = 1
            else:
                endj = 2

            for k in range(starti, endi):
                for l in range(startj, endj):
                    alive_ += grid[i + k][j + l]
                    
            alive[i][j] = alive_
          
    return alive

    # return next_gen(n, grid, alive)


def alive_neighbours_mpi():
    comm = MPI.COMM_WORLD

    size = comm.Get_size()
    rank = comm.Get_rank()
    if rank == 0:
        grid = array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [6, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [7, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [8, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [9, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        ])
        n = len(grid)
        length = {"n": n}
    
        if size > 1:
            
            np = len(grid)
            
            if np % size == 0:
                np = int(np/size)
            else:
                np = int(np/size) + 1
                
            curr = np
            
            for i in range(0, size):
                if i == size - 1:
                    length["len"] = n - (curr - np)
                    comm.send(length, dest=i, tag=1)
                    comm.Send([grid[curr - np: n], MPI.INT], dest=i, tag=11)
                elif i > 0:
                    length["len"] = curr - (curr - np - 1)
                    comm.send(length, dest=i, tag=1)
                    comm.Send([grid[curr - np: curr + 1], MPI.INT], dest=i, tag=11)
         -1
                curr += np
        
        alives = [alive(np + 1, 10, grid[0:np + 1])]
        
       
    elif rank > 0:
        length = comm.recv(source= 0, tag=1)
        grid = empty(shape=(length["len"],length["n"]), dtype=int)
        print(grid.shape)
        comm.Recv([grid, MPI.INT], source=0, tag=11)
        alive_ = alive(length["len"], length["n"], grid)
        print(alive_.shape)
        print(alive_)
        print(rank, type(alive_), type(grid))
        print()
        comm.send(length, dest=0, tag=12)
        comm.Send([alive_, MPI.INT], dest=0, tag=rank)


    if rank == 0:
        for i in range(1, size):
            length = comm.recv(source = i, tag=12)
            print(i, length)
            alive_ = empty(shape=(length["len"],length["n"]), dtype=int)
            print(comm.Recv([alive_, MPI.INT], source=i, tag=i))
            # print(alive_)
            alives.append(alive_)
        return alives


if __name__ == "__main__":
    alive_neighbours_mpi()
    
"""
    
        
        if size > 1:
            if size % 2 == 0:
                for i in range(1, len(alives), 2):
                    length = {i - 1: len(alives[i -1]), i : len(alives[i])}
                    comm.send(length, dest=i, tag=24)
                    comm.Send([array(alives[i-1]), MPI.INT], dest=i, tag=i-1)
                    comm.Send([alives[i], MPI.INT], dest=i, tag=i)
                    print(alives[i-1])
                    print(alives[i])

            else:
                for i in range(1, len(alives, 2)):
                    try:
                    
                        length = {i - 1: len(alives[i -1]), i : len(alives[i])}
                        comm.send(length, dest=i, tag=24)
                        comm.Send([alives[i-1], MPI.INT], dest=i, tag=i -1)
                        comm.Send([alives[i], MPI.INT], dest=i, tag=i)
                        print(alives[i-1])
                    except IndexError:
                        length = {i : len(alives[i])}
                        comm.send(length, dest=i, tag=24)
                        comm.Send([alives[i], MPI.INT], dest=i, tag=i)
        
    elif rank % 2 != 0:
        length = comm.recv(source=0, tag=24)
        alive = []
        for key in length:
            alives_ = empty(shape=(length[key], 10), dtype=int)
            comm.Recv([alives_, MPI.INT], source=0, tag=key)
            print(alives_)
         """
