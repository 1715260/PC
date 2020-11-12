from numpy import array, zeros
from sys import argv
from time import time

# determine the next state of the game
def next_gen(n, grid, alive):
    future = zeros(shape=(n,n), dtype=int)

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0 and alive[i][j] == 3:
                future[i][j] = 1
            elif grid[i][j] == 1 and (alive[i][j] == 3 or alive[i][j] == 2):
                future[i][j] = 1
            
    return future

# calculate the number of alive neighbours
def alive(n, grid):
    alive = zeros(shape=(n,n), dtype=int)
    starti, startj = -1, -1
    endi, endj = 2, 2
    for i in range(0, n):
        for j in range(0, n):
            alive_ = 0
            alive_ -= grid[i][j] # subtract current cell
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
            
            if j == n - 1:
                endj = 1
            else:
                endj = 2

            for k in range(starti, endi):
                for l in range(startj, endj):
                    alive_ += grid[i + k][j + l]
            alive[i][j] = alive_
          


    return next_gen(n, grid, alive)

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
    start = time()
    for _ in range(int(argv[1])):
        grid = alive(len(grid), grid)

    end_time = time() - start

    with open("game_of_life_serial_data.txt", 'a') as f:
        f.write(str(grid))
        f.write("\nsize: 1")
        f.write("\ntime: {}\n\n".format(end_time))
