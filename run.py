#!/usr/bin/python

import sys
import getopt
import os

RUN_PARAMETER = "RUN-NONINTERACTIVE"


def main(argv):

    infile = None
    iterations = 0
    acceptable_distance = 0

    opts, args = getopt.getopt(argv, "f:i:d:")
    for opt, arg in opts:
        if opt == '-f':
            infile = arg
        if opt == '-i':
            iterations = int(arg)
        if opt == '-d':
            acceptable_distance = arg

    os.system("gimp --verbose --debug-handlers --stack-trace-mode always -i -b '(python-fu-agent {} \"{}\" {} {})' -b '(gimp-quit 1)'"
              .format(RUN_PARAMETER, infile, iterations, acceptable_distance))


if __name__ == '__main__':
    main(sys.argv[1:])
