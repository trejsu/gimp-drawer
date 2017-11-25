import time
import numpy as np
import operator


times = dict()


def timed(method):
    def timed_function(*args, **kw):
        start = time.time()
        result = method(*args, **kw)
        end = time.time()
        method_name = "%s.%s" % (method.__module__, method.__name__)
        if method_name not in times:
            times[method_name] = []
        times[method_name].append(end - start)
        # print '%s.%s  %2.2f ms' % (method.__module__, method.__name__, (end - start) * 1000)
        return result
    return timed_function


def print_result():
    average_times = dict(map(lambda (k, v): (k, np.mean(v)), times.iteritems()))
    sorted_times = sorted(average_times.items(), key=operator.itemgetter(1))
    for name, t in sorted_times:
        print name, "%2.2f ms" % (t * 1000)
