mpiexec -n 4 ./ring4 |& tee -a ring4.out
echo ---------ring4 is done-------------

mpiexec -n 4 ./sieve_mpi 3000 |& tee -a sieve_mpi.out
echo ---------sieve_mpi is done-------------


