#!/usr/bin/python

import sys
import getopt
import os

RUN_PARAMETER = "RUN-NONINTERACTIVE"


def main(argv):

    infile = None
    iterations = None
    metric = None

    opts, args = getopt.getopt(argv, "f:i:m:")
    for opt, arg in opts:
        if opt == '-f':
            infile = arg
        if opt == '-i':
            iterations = int(arg)
        if opt == '-m':
            metric = arg

    os.system("gimp -i -b '(python-fu-agent {} \"{}\")' -b '(gimp-quit 1)'".format(RUN_PARAMETER, infile))


if __name__ == '__main__':
    main(sys.argv[1:])
