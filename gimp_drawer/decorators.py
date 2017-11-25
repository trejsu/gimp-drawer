import time


def timed(method):
    def timed_function(*args, **kw):
        start = time.time()
        result = method(*args, **kw)
        end = time.time()
        print '%s.%s  %2.2f ms' % (method.__module__, method.__name__, (end - start) * 1000)
        return result
    return timed_function
