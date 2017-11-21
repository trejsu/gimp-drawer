#!/usr/bin/python

import sys
import getopt
import os

RUN_PARAMETER = "RUN-NONINTERACTIVE"


def main(argv):

    infile = None
    corrections = 0
    acceptable_distance = 0
    verbose = False

    opts, args = getopt.getopt(argv, "f:i:d:v")
    for opt, arg in opts:
        if opt == '-f':
            infile = arg
        if opt == '-i':
            corrections = int(arg)
        if opt == '-d':
            acceptable_distance = arg
        if opt == '-v':
            verbose = True

    command = "gimp {} -i -b '(python-fu-agent {} \"{}\" {} {})' -b '(gimp-quit 1)'"\
        .format("--verbose --debug-handlers --stack-trace-mode always" if verbose else "",
                RUN_PARAMETER, infile, corrections, acceptable_distance)

    os.system(command)


if __name__ == '__main__':
    main(sys.argv[1:])
