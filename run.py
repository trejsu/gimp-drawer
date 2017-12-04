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
    render_mode = 0

    opts, args = getopt.getopt(argv, "i:d:vm:r:")
    for opt, arg in opts:
        if opt == '-i':
            infile = arg
        if opt == '-d':
            acceptable_distance = arg
        if opt == '-v':
            verbose = True
        if opt == '-m':
            mode = arg
        if opt == '-r':
            render_mode = arg

    command = "environment {} -i -b '(python-fu-agent {} \"{}\" {} {} {})' -b '(environment-quit 1)'"\
        .format("--verbose --debug-handlers --stack-trace-mode always" if verbose else "",
                RUN_PARAMETER, infile, acceptable_distance, mode, render_mode)
    os.system(command)


if __name__ == '__main__':
    main(sys.argv[1:])
