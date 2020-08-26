# !/usr/bin/env python3

"""
Weak scaling
------------
Weak scaling is defined as how the solution time varies with the number of processors for a fixed
problem size per processor.

Strong scaling
--------------
Strong scaling is defined as how the solution time varies with the number of processors for a fixed
total problem size.

Throughput
----------
Throughput is the number of tasks it can be complete in a given amount of time. Throughput is expressed
in actions per unit of time. Throughput is related to another important metric, called latency, which is
the amount of time it takes to execute a task from beginning to end. Latency is measured in units of time.


Speedup
-------
A metric that's commonly used to measure the effectiveness of a parallel program is speedup, which is related
to the program's efficiency. Speedup is calculated as a ratio of the time it takes to execute the program in
the optimal sequential manner with just one worker or a single processor, over the time it takes to execute
in a parallel manner with a certain number of parallel processors.

Amdahl's law
------------
There is a well-known equation for estimating the speedup that a parallel program can achieve called Amdahl's law,
which is named after the computer scientist that formulated it. This states that the overall performance improvement
gained by optimizing a single part of a system is limited by the fraction of time that the improved part is actually
used.


https://en.wikipedia.org/wiki/Amdahl%27s_law
https://www.youtube.com/watch?v=BxH93LTSOFo
https://www.youtube.com/watch?v=KAfiOjGUl6o


Efficiency:
----------
Another metric to consider is efficiency, which indicates how well system resources, like additional processors,
are utilized. We can get a rough calculation for efficiency by dividing the speedup by the number of processors.
"""

""" Measure the speedup of a parallel algorithm """

from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp
import time


# sequential implementation
def seq_sum(lo, hi):
    return sum(range(lo, hi))


# parallel implementation
def par_sum(lo, hi, pool=None):
    # if the pool argument is None, this indicates intial call to the function
    # if pool is None the condition evaluates to true and we create ProcessPool Executor
    # not None == Not False == True
    if not pool:
        with ProcessPoolExecutor() as executor:
            futures = par_sum(lo, hi, pool=executor)
            # Retrive the individual results and sum them
            # summing over all sub-divided results in the
            # as_completed() returns a iterator that yields futures from
            # the list of futures as the complete
            return sum(f.result() for f in as_completed(futures))
    else:
        # base case threshold
        # Base Case => Increase => Parallel efficiency Increase
        # Base Case => Decrease => Parallel efficiency Decrease
        if hi - lo <= 100_000:
            return [pool.submit(sum, range(lo, hi))]
        else:
            mid = (hi + lo) // 2  # middle index for splitting
            left = par_sum(lo, mid, pool=pool)
            right = par_sum(mid, hi, pool=pool)
            return left + right


if __name__ == '__main__':
    NUM_EVAL_RUNS = 1
    SUM_VALUE = 100_000_000

    print('Evaluating Sequential Implementation...')

    # "warm up"
    sequential_result = seq_sum(1, SUM_VALUE)

    sequential_time = 0
    for i in range(NUM_EVAL_RUNS):
        start = time.perf_counter()
        # sequential summing
        seq_sum(1, SUM_VALUE)
        sequential_time += time.perf_counter() - start
    sequential_time /= NUM_EVAL_RUNS

    print('Evaluating Parallel Implementation...')
    # "warm up"
    parallel_result = par_sum(1, SUM_VALUE)
    parallel_time = 0
    for i in range(NUM_EVAL_RUNS):
        start = time.perf_counter()
        par_sum(1, SUM_VALUE)
        parallel_time += time.perf_counter() - start
    parallel_time /= NUM_EVAL_RUNS

    if sequential_result != parallel_result:
        raise Exception('sequential_result and parallel_result do not match.')
    print('Average Sequential Time: {:.2f} ms'.format(sequential_time * 1000))
    print('Average Parallel Time: {:.2f} ms'.format(parallel_time * 1000))
    print('Speedup: {:.2f}'.format(sequential_time / parallel_time))
    print('Efficiency: {:.2f}%'.format(100 * (sequential_time / parallel_time) / mp.cpu_count()))
