#!/usr/bin/python

import sys
import getopt
import os

RUN_PARAMETER = "RUN-NONINTERACTIVE"


def main(argv):

    source = None
    acceptable_distance = 0
    verbose = False
    render_mode = 0
    input_file = None
    seed = 0

    # todo: change to full names
    opts, args = getopt.getopt(argv, "s:d:vr:i:x:")
    for opt, arg in opts:
        if opt == '-s':
            source = arg
        if opt == '-d':
            acceptable_distance = arg
        if opt == '-v':
            verbose = True
        if opt == '-m':
            mode = arg
        if opt == '-r':
            render_mode = arg
        if opt == '-i':
            input_file = arg
        if opt == '-x':
            seed = arg

    command = "gimp {} -i -b '(python-fu-agent {} \"{}\" {} {} \"{}\" {})' -b '(gimp-quit 1)'"\
        .format("--verbose --debug-handlers --stack-trace-mode always" if verbose else "",
                RUN_PARAMETER, source, acceptable_distance, render_mode, input_file, seed)
    os.system(command)


if __name__ == '__main__':
    main(sys.argv[1:])
