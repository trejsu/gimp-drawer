#!/usr/bin/python

import sys
import getopt
import os

RUN_PARAMETER = "RUN-NONINTERACTIVE"


def main(argv):

    infile = None
    acceptable_distance = 0
    verbose = False
    mode = 0

    opts, args = getopt.getopt(argv, "i:d:vm:")
    for opt, arg in opts:
        if opt == '-i':
            infile = arg
        if opt == '-d':
            acceptable_distance = arg
        if opt == '-v':
            verbose = True
        if opt == '-m':
            mode = arg

    command = "gimp {} -i -b '(python-fu-agent {} \"{}\" {} {} {})' -b '(gimp-quit 1)'"\
        .format("--verbose --debug-handlers --stack-trace-mode always" if verbose else "",
                RUN_PARAMETER, infile, 0, acceptable_distance, mode)
    os.system(command)


if __name__ == '__main__':
    main(sys.argv[1:])
