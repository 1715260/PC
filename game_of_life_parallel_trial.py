from mpi4py import MPI
from sys import argv
from numpy import array, empty, concatenate, zeros
from time import time

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


def merge(n, m, grid, np=1):
    
    np_ = int(2**np)
    diff = int(np_/2)
    surplus = False
    if np_ <= size:
        processor = [i for i in range(0, size, np_)]
        sender = [i + diff for i in processor]

        if rank in sender:
            a, b = grid.shape
            shape = array([a, b])
            comm.Isend([shape, MPI.INT], dest=rank-diff, tag=44)

            req = comm.Isend([grid, MPI.INT], dest=rank-diff, tag=33)
        
        elif rank in processor:
            shape = empty(shape=(2), dtype=int)
            req = comm.Irecv([shape, MPI.INT], source=rank+diff, tag=44)
            req.wait()
            grid_ = empty(shape=(shape[0], shape[1]), dtype=int)
            req = comm.Irecv([grid_, MPI.INT], rank+diff, tag=33)
            req.wait()
            return merge(n, m, array([*grid[:-1], *grid_]), np=np+1)


    return grid
        


def next_gen(n, m, grid, alive):
    future = zeros(shape=(n, m), dtype=int)

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 0 and alive[i][j] == 3:
                future[i][j] = 1
            elif grid[i][j] == 1 and (alive[i][j] == 3 or alive[i][j] == 2):
                future[i][j] = 1

    return future

def compare(n, grid1, grid2, grid3):
    alive1 = alive(3, n, array([grid1, grid2, grid3]), merge=False)
    return alive1[1]

def merge_alive(m, n, grid, alive):
    if rank == 0:
        grid_ = empty(shape=(n), dtype=int)
        comm.Isend([grid[-2], MPI.INT], dest=rank+1, tag =1)
        req = comm.Irecv([grid_, MPI.INT], source=rank+1, tag=2)
        req.wait()
        alive[-1] = compare(n, grid[-2], grid[-1], grid_)

        grid = next_gen(m, n, grid, alive)
        return merge(m, n, grid)
    elif rank == size - 1:
        grid_ = empty(shape=(n), dtype=int)
        comm.Isend([grid[1], MPI.INT], dest=rank-1, tag=2)
        req = comm.Irecv([grid_, MPI.INT], source=rank -1, tag=1)
        req.wait()
        alive[0] = compare(n, grid_, grid[0], grid[1])

        grid = next_gen(m, n, grid, alive)
        return merge(m, n, grid)
    else:
        grid_ = empty(shape=(n), dtype=int)
        grid_2 = empty(shape=(n), dtype=int)
        comm.Isend([grid[-2], MPI.INT], dest=rank + 1, tag=1)
        comm.Isend([grid[1], MPI.INT], dest=rank - 1, tag=2)
        req1 = comm.Irecv([grid_, MPI.INT], source=rank + 1, tag=2)
        req2 = comm.Irecv([grid_2, MPI.INT], source= rank - 1, tag=1)

        req1.wait()
        req2.wait()

        alive[-1] = compare(n, grid[-2], grid[-1], grid_)
        alive[0] = compare(n, grid_, grid[0], grid[1])
        
        grid=next_gen(m, n, grid, alive)
        return merge(m, n, grid)


# calculate the number of alive neighbours
def alive(n, m, grid, merge=True):
    alive = zeros(shape=(n, m), dtype=int)
    starti, startj = -1, -1
    endi, endj = 2, 2
    for i in range(0, n):
        for j in range(0, m):
            alive_ = 0
            alive_ -= grid[i][j]  # subtract current cell
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

    if merge:
        return merge_alive(n, m, grid, alive)
        
    else:
        return alive

def alive_mpi(size, n, grid):

    np = int(n/size) 
    

    for i in range(size):
        if rank == i:
            if i == size - 1:
                return alive(n - rank*np, n, grid[rank*np:])
                # merge_alive(n, grid, grid[rank*np:])
            else:
                return alive(rank*np - rank*np + np + 1, n,
                      grid[rank*np:rank*np + np + 1])
                # merge_alive(n, grid, grid[rank*np:rank*np + np + 1])

def broadcast(size, n, grid):
    if rank == 0:
        for i in range(size):
            comm.Isend([grid, MPI.INT], dest=i, tag=23)
    else:
        req = comm.Irecv([grid, MPI.INT], source=0, tag=23)
        return grid

if __name__ == "__main__":
    grid = array([
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    ])
    start_time = time()
    for _ in range(int(argv[1])):
        if rank == 0:
            grid = alive_mpi(size, 10, grid)
            broadcast(size, 10, grid)
        else:
            grid = broadcast(size, 10, grid)
            if rank == 3:
                print(grid)
            alive_mpi(size, 10, grid)

    if rank == 0:
        end_time = time() - start_time

        with open("game_of_life_parallel_data.txt", 'a') as f:
            f.write(str(grid))
            f.write("\nsize: {}".format(size))
            f.write("\ntime: {}\n\n".format(end_time))