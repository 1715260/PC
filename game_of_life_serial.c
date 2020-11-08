#include <stdio.h>

void print_grid(int n, int grid[n][n]){
   
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            printf("%d ", grid[i][j]);
        }
        printf("\n\n\n\n");
    }
}

void next_generation(int n, int grid[n][n]){
    int future[n][n];
    // testing for 
    for (int i = 0; i < n; i++){
        for (int j = 1; j < n; j++){
            // Finding out number of alive neighbours
            int alive = 0;
            alive -= grid[i][j];
            for (int k = -1; k <= 1; k++){
                for (int l = -1; l <= 1; l++){
                    alive += grid[i + k][j + l];
                }
            }
            printf("%d are alive\n", alive);
            if ((grid[i][j] == 1) && (alive < 2)){
                future[i][j] = 0;
            }
            else if ((grid[i][j] == 1) && (alive > 3)){
                future[i][j] = 0;
            }
            else if ((grid[i][j] == 0) && (alive == 3)){
                future[i][j] = 1;
            }
            else{
                future[i][j] = grid[i][j];
            }
        }
    }

    print_grid(n, future);
}
int main(int argc, char *argv[]){
    // Note outside square is not active, strictly to avoid seg faults
    // Therefore actual playing field is 8x8
    int grid[10][10]  = {
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 1, 1, 0, 0, 0, 0, 0, 0, 0},
        {0, 1, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 1, 1, 0, 0, 0, 0},
        {0, 0, 0, 1, 1, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 1, 0, 0, 0},
        {0, 0, 0, 0, 0, 1, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    };

    // print_grid(10, 10, grid);
    // print_grid(5, 10, 10, grid);
    next_generation(10, grid);
    

}