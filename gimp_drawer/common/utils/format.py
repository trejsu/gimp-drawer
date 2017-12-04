from gimp_drawer.common.decorators.timed import timed


@timed
def format_time(seconds):
    minutes = seconds / 60
    hours = seconds / 3600
    if minutes < 1:
        return "%.1f" % seconds + "s"
    elif hours < 1:
        return "%.1f" % minutes + "m"
    return "%.1f" % hours + "h"
