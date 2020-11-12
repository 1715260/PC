from numpy import array
from time import time
from os import system

if __name__ == "__main__":
    for i in range(100):
        system("python game_of_life_serial_copy.py {}".format(i))
        print(i)

    for size in range(0, 4, 2):
        for i in range(100):
            system("mpiexec -n {} python game_of_life_parallel_trial.py {}".format(size, i))
            print(size, i)