#!/usr/bin/python

import sys
import getopt
import os

RUN_PARAMETER = "RUN-NONINTERACTIVE"


def main(argv):

    source = None

    opts, args = getopt.getopt(argv, "s:")
    for opt, arg in opts:
        if opt == '-s':
            source = arg

    command = "gimp -i -b '(python-fu-image-generator {} \"{}\")' -b '(gimp-quit 1)'"\
        .format(RUN_PARAMETER, source)
    os.system(command)


if __name__ == '__main__':
    main(sys.argv[1:])
