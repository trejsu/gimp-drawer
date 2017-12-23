#!/usr/bin/python

import sys
import getopt
import os
import random

RUN_PARAMETER = "RUN-NONINTERACTIVE"


def main(argv):

    source = None
    acceptable_distance = 0
    verbose = False
    render_mode = 0
    input_file = None
    seed = random.randint(0, 2**32 - 1)
    actions = sys.maxint

    # todo: change to full names
    opts, args = getopt.getopt(argv, "s:d:vr:i:x:a:")
    for opt, arg in opts:
        if opt == '-s':
            source = arg
        if opt == '-d':
            acceptable_distance = arg
        if opt == '-v':
            verbose = True
        if opt == '-r':
            render_mode = arg
        if opt == '-i':
            input_file = arg
        if opt == '-x':
            seed = arg
        if opt == '-a':
            actions = arg

    command = "gimp {} -i -b '(python-fu-agent {} \"{}\" {} {} \"{}\" {} {})' -b '(gimp-quit 1)'"\
        .format("--verbose --debug-handlers --stack-trace-mode always" if verbose else "",
                RUN_PARAMETER, source, acceptable_distance, render_mode, input_file, seed, actions)
    os.system(command)


if __name__ == '__main__':
    main(sys.argv[1:])
