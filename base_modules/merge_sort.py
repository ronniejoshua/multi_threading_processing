#!/usr/bin/env python3
""" Solution: Sort an array of random integers with merge sort """

import random
import time
import multiprocessing as mp
import math


def seq_merge_sort(array, *args):
    """ sequential implementation of merge sort """
    # It's the first call
    # If args is not provided => Not False(None/Empty is False) => True
    if not args:
        # sort the array/Recursive Call
        seq_merge_sort(array, 0, len(array) - 1)
        # return the sorted array
        return array
    else:
        # recursive call
        left, right = args
        if left < right:
            # find the middle point
            mid = (left + right) // 2
            # sort the left half
            seq_merge_sort(array, left, mid)
            # sort the right half
            seq_merge_sort(array, mid + 1, right)
            # merge the two sorted halves
            merge(array, left, mid, right)


def merge(array, left, mid, right):
    """ helper method to merge two sorted subarrays
        array[l..m] and array[m+1..r] into array """

    # copy data to temp subarrays to be merged
    left_temp_arr = array[left:mid + 1].copy()
    right_temp_arr = array[mid + 1:right + 1].copy()

    # initial indexes for left, right and merged subarrays
    left_temp_index = 0
    right_temp_index = 0
    merge_index = left

    # merge temp arrays into original
    while left_temp_index < (mid - left + 1) or right_temp_index < (right - mid):
        if left_temp_index < (mid - left + 1) and right_temp_index < (right - mid):
            if left_temp_arr[left_temp_index] <= right_temp_arr[right_temp_index]:
                array[merge_index] = left_temp_arr[left_temp_index]
                left_temp_index += 1
            else:
                array[merge_index] = right_temp_arr[right_temp_index]
                right_temp_index += 1

        # copy any remaining on left side
        elif left_temp_index < (mid - left + 1):
            array[merge_index] = left_temp_arr[left_temp_index]
            left_temp_index += 1

        # copy any remaining on right side
        elif right_temp_index < (right - mid):
            array[merge_index] = right_temp_arr[right_temp_index]
            right_temp_index += 1
        merge_index += 1


def par_merge_sort(array, *args):
    """ parallel implementation of merge sort """
    if not args:  # first call
        shared_array = mp.RawArray('i', array)
        # Initial Recursive Call
        # The following function does not return any value
        # It mutates the array/list
        # Final argument is dept of recursion
        par_merge_sort(shared_array, 0, len(array) - 1, 0)
        # insert result into original array
        array[:] = shared_array
        return array
    else:
        left, right, depth = args
        # If the recursion depth is >= the number of processors
        # then use the sequential merge sort algorithm
        if depth >= math.log(mp.cpu_count(), 2):
            seq_merge_sort(array, left, right)
        elif left < right:
            # find the middle point
            mid = (left + right) // 2
            left_proc = mp.Process(target=par_merge_sort, args=(array, left, mid, depth + 1))
            left_proc.start()
            # Uses current process to recursively sort the right half
            par_merge_sort(array, mid + 1, right, depth + 1)
            left_proc.join()
            # merge the two sorted halves
            merge(array, left, mid, right)


if __name__ == '__main__':
    NUM_EVAL_RUNS = 1
    print('Generating Random Array...')
    array = [random.randint(0, 10_000) for i in range(1_000_000)]

    print('Evaluating Sequential Implementation...')
    sequential_result = seq_merge_sort(array.copy())
    sequential_time = 0
    for i in range(NUM_EVAL_RUNS):
        start = time.perf_counter()
        seq_merge_sort(array.copy())
        sequential_time += time.perf_counter() - start
    sequential_time /= NUM_EVAL_RUNS

    print('Evaluating Parallel Implementation...')
    parallel_result = par_merge_sort(array.copy())
    parallel_time = 0
    for i in range(NUM_EVAL_RUNS):
        start = time.perf_counter()
        par_merge_sort(array.copy())
        parallel_time += time.perf_counter() - start
    parallel_time /= NUM_EVAL_RUNS

    if sequential_result != parallel_result:
        raise Exception('sequential_result and parallel_result do not match.')
    print('Average Sequential Time: {:.2f} ms'.format(sequential_time * 1000))
    print('Average Parallel Time: {:.2f} ms'.format(parallel_time * 1000))
    print('Speedup: {:.2f}'.format(sequential_time / parallel_time))
    print('Efficiency: {:.2f}%'.format(100 * (sequential_time / parallel_time) / mp.cpu_count()))
