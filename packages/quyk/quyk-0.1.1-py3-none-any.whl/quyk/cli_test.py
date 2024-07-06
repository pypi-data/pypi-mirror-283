import sys

registered_functions = {}

def cli_test(test_args=None):
    def decorator(func):
        func_name = func.__name__
        registered_functions[func_name] = (func, test_args)
        return func
    return decorator
