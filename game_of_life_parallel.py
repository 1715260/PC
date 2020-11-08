from mpi4py import MPI
from numpy import array, zeros, empty
from sys import argv


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

if __name__ == "__main__":

    comm = MPI.COMM_WORLD

    size = comm.Get_size()
    rank = comm.Get_rank()
    if rank == 0:
        # print(size)
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
        #comm.send(length, dest=1, tag=1)
        #comm.Send([grid, MPI.INT], dest=1, tag=11)
    
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
                    # print(i, length)
                    comm.send(length, dest=i, tag=1)
                    comm.Send([grid[curr - np: n], MPI.INT], dest=i, tag=11)
                elif i > 0:
                    length["len"] = curr - (curr - np - 1)
                    # print("{}\t{}".format(length["len"], curr - (curr - np - 1)))
                    # print("{}\n\t{}\n\n".format(grid[curr - np - 1: curr + 1], grid[curr - np: curr + 1]))
                    comm.send(length, dest=i, tag=1)
                    comm.Send([grid[curr - np: curr + 1], MPI.INT], dest=i, tag=11)
        
                curr += np
        
        alive_ = alive(np + 1, 10, grid[0:np + 1])
        print(grid[0:np])
        # print("from 0\n{}\n\n".format(alive_))
        # print(np)
    elif rank > 0:
        # print(rank)
        length = comm.recv(source= 0, tag=1)
        grid = empty(shape=(length["len"],length["n"]), dtype=int)
        comm.Recv([grid, MPI.INT], source=0, tag=11)
        # print(rank, rank*3, rank*3 - 1)
        #print(length)
        # print(grid.shape)
        alive_ = alive(length["len"], length["n"], grid)
        print("{}\n{}\n{}\n\n".format(rank, length, grid))