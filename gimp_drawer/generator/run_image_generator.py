#!/usr/bin/python

import sys
import getopt
import os

RUN_PARAMETER = "RUN-NONINTERACTIVE"


def main(argv):

    source = None
    action_type = -1
    limit = -1

    opts, args = getopt.getopt(argv, "s:a:l:")
    for opt, arg in opts:
        if opt == '-s':
            source = arg
        if opt == '-a':
            action_type = arg
        if opt == '-l':
            limit = arg

    print "before command"

    command = "gimp -i -b '(python-fu-image-generator {} \"{}\" {} {})' -b '(gimp-quit 1)'"\
        .format(RUN_PARAMETER, source, action_type, limit)
    os.system(command)


if __name__ == '__main__':
    main(sys.argv[1:])
