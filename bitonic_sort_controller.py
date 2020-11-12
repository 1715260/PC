from os import system

if __name__ == "__main__":
   
    
    for i in range(10):
        for size in range(3, 23):
            system("python bitonic_serial.py {}".format(size))


    for i in range(10):
        for np in range(0,4, 2):
            for size in range(3, 23):
                system("mpiexec -n {} python bitonic_sort_parallel_attempt_3.py {}".format(np, size))
    
