P1 = sieve_mpi
CC = mpicc

all: $(P1) ring4

ring4: mpi_ring_v4.c
	$(CC) mpi_ring_v4.c -o ring4

sieve_mpi: $(P1).c
	$(CC) sieve_mpi.c -o sieve_mpi -lm

clean:
	rm -vf ring4 $(P1)
