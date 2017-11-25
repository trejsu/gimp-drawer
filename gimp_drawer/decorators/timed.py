import time
import numpy as np
import operator


TIMES = dict()


def timed(method):
    def timed_function(*args, **kw):
        start = time.time()
        result = method(*args, **kw)
        end = time.time()
        method_name = "%s.%s" % (method.__module__, method.__name__)
        if method_name not in TIMES:
            TIMES[method_name] = []
        TIMES[method_name].append(end - start)
        return result
    return timed_function


def print_result():
    summary_times = dict(map(lambda (k, v): (k, np.sum(v)), TIMES.iteritems()))
    sorted_times = sorted(summary_times.items(), key=operator.itemgetter(1))
    for name, t in sorted_times:
        print name, "%2.2f s" % t
