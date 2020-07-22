from functools import wraps
import time


def timer(func):
    # Enclosing Scope for the Wrapper function

    # @wraps(func) Returns the target functions functionality
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Do something before the func execution
        start_time = time.perf_counter()

        # func execution
        value = func(*args, **kwargs)

        # Do something after the func execution
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print("Finished {} in {} secs".format(repr(func.__name__), round(run_time, 3)))

        # Return the executed func
        return value

    return wrapper


def debug(func):
    """Print the function signature and return value"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")

        value = func(*args, **kwargs)

        print(f"{func.__name__!r} returned {value!r}")
        return value

    return wrapper
