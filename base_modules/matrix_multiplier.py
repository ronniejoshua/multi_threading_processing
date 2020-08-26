#!/usr/bin/env python3

""" sequential implementation of matrix multiplication """

"""
Solution: Matrix multiply in Python

To design our parallel solution for the matrix multiplication challenge, we began with domain decomposition to 
consider the ways we could partition the problem. One very convenient aspect of matrix multiplication is that 
every element of the result matrix C can be calculated independently. 

Calculating the individual elements of C for a four by three result matrix can be partitioned into 12 independent 
tasks. This type of problem is sometimes called embarrassingly parallel because it breaks apart so easily and doesn't 
require communication between each of the tasks. That can turn into a lot of tasks, especially for a large result 
matrix. So we decided to agglomerate those tasks based on row and will modify the number of rows in each group at 
run time, based on the number of processors that are available in the computer. 

If the system only has two processors, then we'll combine the computation into two tasks. If it has four processors, 
then that's four tasks, and so on. 

Since these computations are CPU-intensive, we'll be using Python's multi-processing package to create tasks as 
separate processes rather than separate threads to get around the limitations of the Global Interpreter Lock. 
"""

import random
import time
import math
import multiprocessing as mp


def seq_matrix_multiply(A, B):
    # establish a few useful variables
    num_rows_A = len(A)
    num_cols_A = len(A[0])
    num_rows_B = len(B)
    num_cols_B = len(B[0])
    if num_cols_A != num_rows_B:
        raise ArithmeticError(
            f"Invalid dimensions; Cannot multiply {num_rows_A}x{num_cols_A}*{num_rows_B}x{num_cols_B}")
    # compute a return matrix product C = A*B
    C = [[0] * num_cols_B for i in range(num_rows_A)]
    for i in range(num_rows_A):
        for j in range(num_cols_B):
            for k in range(num_cols_A):  # same as num_rows_B
                C[i][j] += A[i][k] * B[k][j]
    return C


# parallel implementation of matrix multiplication
def par_matrix_multiply(A, B):
    # establish a few useful variables
    num_rows_A = len(A)
    num_cols_A = len(A[0])
    num_rows_B = len(B)
    num_cols_B = len(B[0])
    if num_cols_A != num_rows_B:
        raise ArithmeticError(
            f"Invalid dimensions; Cannot multiply {num_rows_A}x{num_cols_A}*{num_rows_B}x{num_cols_B}")

    # if the output C will be small enough, simply use the sequential version
    if num_rows_A * num_cols_B < 25_000:
        return seq_matrix_multiply(A, B)

    # create workers to calculate results for subset of rows in C

    # get the number of available processors
    num_workers = mp.cpu_count()
    print(f"get the number of available processors: {num_workers}")
    # divide the rows of the output matrix into roughly equal-sized chunks
    chunk_size = math.ceil(num_rows_A / num_workers)

    """
    initialized a shared memory array to hold the elements of the result matrix C, so that each of the helper par 
    worker processes can put their portion of the result directly into it.
    
    Python's multiprocessing package provides two options to allocate an array of shared memory that can be accessed 
    by multiple processes. The standard multiprocessing array uses a lock to synchronize access among the processes 
    to prevent a data erase. The multiprocessing.RawArray on the other hand, does not include synchronization. 
    
    If multiple processes would be reading and writing the same array elements, then you should stick with the array 
    that has built-in synchronization. However, we determined that the matrix multiplication is embarrassingly 
    parallel and that the calculation for each output element could be treated as a completely independent task. 
    So, we decided to use a raw array because it allows the program to run a lot faster because it doesn't have to 
    deal with synchronization.
    
    the shared memory array is only one-dimensional. We named it C_1D and treated its contents as a flattened version 
    of the 2D result matrix. Each of the parallel worker processes were assigned a portion of the one-dimensional C 
    array to fill in with results. And then at the end, we converted the flattened one-dimensional C array into a 
    two-dimensional list of lists as the final output.
    """
    C_1D = mp.RawArray('d', num_rows_A * num_cols_B)
    workers = []
    for w in range(num_workers):
        row_start_C = min(w * chunk_size, num_rows_A)
        row_end_C = min((w + 1) * chunk_size, num_rows_A)
        workers.append(mp.Process(target=_par_worker,
                                  args=(A, B, C_1D, row_start_C, row_end_C)))
    for w in workers:
        w.start()
    for w in workers:
        w.join()

    # convert flat resultant matrix C_1D into 2D list-of-lists
    C_2D = [[0] * num_cols_B for i in range(num_rows_A)]
    for i in range(num_rows_A):
        for j in range(num_cols_B):
            C_2D[i][j] = C_1D[i * num_cols_B + j]
    return C_2D


# Parallel worker to calculate results for subset of rows in C
def _par_worker(A, B, C_1D, row_start_C, row_end_C):
    # subset of rows in A
    for i in range(row_start_C, row_end_C):
        # num_cols_B
        for j in range(len(B[0])):
            # num_cols_A, also num_rows_B
            for k in range(len(A[0])):
                C_1D[i * len(B[0]) + j] += A[i][k] * B[k][j]


if __name__ == '__main__':
    NUM_EVAL_RUNS = 1
    row_dim = 500
    col_dim = 500
    A = [[random.random() for i in range(col_dim)] for j in range(row_dim)]
    B = [[random.random() for i in range(col_dim)] for j in range(row_dim)]

    print('Evaluating Sequential Implementation...')
    # "warm up"
    sequential_result = seq_matrix_multiply(A, B)
    sequential_time = 0
    for i in range(NUM_EVAL_RUNS):
        start = time.perf_counter()
        seq_matrix_multiply(A, B)
        sequential_time += time.perf_counter() - start
    sequential_time /= NUM_EVAL_RUNS

    print('Evaluating Parallel Implementation...')
    # "warm up"
    parallel_result = par_matrix_multiply(A, B)
    parallel_time = 0
    for i in range(NUM_EVAL_RUNS):
        start = time.perf_counter()
        par_matrix_multiply(A, B)
        parallel_time += time.perf_counter() - start
    parallel_time /= NUM_EVAL_RUNS

    if sequential_result != parallel_result:
        raise Exception('sequential_result and parallel_result do not match.')
    print('Average Sequential Time: {:.2f} ms'.format(sequential_time * 1000))
    print('Average Parallel Time: {:.2f} ms'.format(parallel_time * 1000))
    print('Speedup: {:.2f}'.format(sequential_time / parallel_time))
    print('Efficiency: {:.2f}%'.format(100 * (sequential_time / parallel_time) / mp.cpu_count()))
