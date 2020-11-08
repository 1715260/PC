from numpy import array, zeros



def next_generation(n, grid):
    future = zeros(shape=(n,n))
    
    for i in range(1, n - 1):
        for j in range(1, n -1):
           # print("{} ".format(grid[i][j]))
            alive = 0;
            alive -= grid[i][j]
            
            for k in range(-1, 2):
                for l in range(-1, 2):
                    alive += grid[i + k][j + l]
                   
        
            if grid[i][j] == 0 and alive == 3:
                future[i][j] = 1
            elif grid[i][j] == 1 and (alive == 3 or alive == 2):
                future[i][j] = 1
    print(future)
if __name__ == "__main__":
    grid = array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    
    next_generation(len(grid), grid)