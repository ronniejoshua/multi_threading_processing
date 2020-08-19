#!/usr/bin/env python3
""" Recursively sum a range of numbers """

"""
Divide and conquer

One class of algorithms that are well-suited for parallel execution across multiple processors are divide and conquer 
algorithms. They work by first dividing a large problem into a number of smaller subproblems of roughly equal size. 

Next, the conquer phase recursively solves each of those subproblems, and finally, the solution to the subproblems 
are combined together to produce the overall solution for the original problem. The common structure for dividing 
conquered code usually consists of an if/else statement. If the algorithm has reached what's called a base case, 
meaning the problem has been subdivided into a small enough piece to solve directly, then simply solve it. 

Otherwise, following the else case, divide the current problem into two smaller pieces referred to as the 
left and right problems. Solve both of those problems recursively using the same divide and conquer strategy. Then, 
combine the left and right solutions. Consider the task of summing together a large number of elements.
 
Divide and conquer algorithms lend themselves to being made parallel because each of the subproblems are independent,
so they can be executed in parallel on different processors. Now, just because a divide and conquer algorithm can be 
made parallel doesn't mean it's always advantageous to do so. Depending on the size of the problem set and the 
complexity of the operations involved, the cost and overhead involved in making the algorithm parallel may outweigh 
the potential benefits.

Summing together numbers is a cpu intensive operation. So, to get around Python's global interpreter lock, I'll need 
to implement this using multiple processes. 
"""

from concurrent.futures import ProcessPoolExecutor, as_completed


def sq_recursive_sum(low, high):
    # base case threshold
    if high - low <= 100_000:
        return sum(range(low, high))
    else:
        # middle index for splitting
        mid = (low + high) // 2
        left_half = sq_recursive_sum(low, mid)
        right_half = sq_recursive_sum(mid, high)
        return left_half + right_half


def pc_recursive_sum(low, high, pool=None):
    # if the pool argument is None, this indicates intial call to the function
    # if pool is none the condition evaluates to true and we create ProcessPool Executor
    # not None == Not False == True
    if not pool:
        with ProcessPoolExecutor() as executor:
            futures = pc_recursive_sum(low, high, pool=executor)
            # Retrive the individual results and sum them
            # summing over all sub-divided results in the
            # as_completed() returns a iterator that yields futures from
            # the list of futures as the complete
            return sum(f.result() for f in as_completed(futures))
    else:
        # base case threshold
        if high - low <= 100_000:
            # submitting the sum(range(low, high) to the process pool
            # this returns a future object. We use list comprehension to return a list
            # containing future object
            return [pool.submit(sum, range(low, high))]
        else:
            # middle index for splitting
            mid = (low + high) // 2
            left_half = pc_recursive_sum(low, mid, pool=pool)
            right_half = pc_recursive_sum(mid, high, pool=pool)
            # the base case returns a list and list can be concatenated
            # hence this returns a list containing all of the subdivided tasks
            return left_half + right_half


if __name__ == '__main__':
    total = pc_recursive_sum(1, 1_000_000_000)
    print('Total sum via pc_recursive_sum is', total)

    total = sq_recursive_sum(1, 1_000_000_000)
    print('Total sum via sq_recursive_sum is', total)
