import time
import numpy as np
import operator
from config import timers


TIMES = dict()


def timed(method):
    def timed_function(*args, **kw):
        if timers:
            start = time.time()
            result = method(*args, **kw)
            end = time.time()
            method_name = "%s.%s" % (method.__module__, method.__name__)
            if method_name not in TIMES:
                TIMES[method_name] = []
            TIMES[method_name].append(end - start)
            return result
        return method(*args, **kw)

    return timed_function


def print_result():
    # summary_times = dict(map(lambda (k, v): (k, np.sum(v)), TIMES.iteritems()))
    summary_times = dict([(k, np.sum(v)) for k, v in TIMES.iteritems()])
    sorted_times = sorted(summary_times.items(), key=operator.itemgetter(1))
    for name, t in sorted_times:
        print name, "%2.2f s" % t
