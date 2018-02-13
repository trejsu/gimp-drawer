#!/usr/bin/python

import sys
import getopt
import os

RUN_PARAMETER = "RUN-NONINTERACTIVE"


def main(argv):

    path = None
    action_type = -1
    limit = -1
    size = 300
    diffs = 0

    opts, args = getopt.getopt(argv, "p:a:l:s:d")
    for opt, arg in opts:
        if opt == '-p':
            path = arg
        if opt == '-a':
            action_type = arg
        if opt == '-l':
            limit = arg
        if opt == '-s':
            size = arg
        if opt == '-d':
            diffs = 1

    command = "gimp -i -b '(python-fu-image-dataset {} \"{}\" {} {} {} {})' -b '(gimp-quit 1)'"\
        .format(RUN_PARAMETER, path, action_type, limit, size, diffs)
    os.system(command)


if __name__ == '__main__':
    main(sys.argv[1:])
