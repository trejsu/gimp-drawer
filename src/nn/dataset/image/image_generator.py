import argparse
import os

ARGS = None


def main():
    command = "gimp -i -b '(python-fu-image-generator " \
              "RUN-NONINTERACTIVE \"{}\" {} {} {} {})' -b '(gimp-quit 1)'"\
              .format(ARGS.path, ARGS.action, ARGS.limit, ARGS.size, int(ARGS.diffs))
    os.system(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--path", type=str, help="Path to the directory with data")
    parser.add_argument("-a", "--action", type=int, default=-1,
                        help="Number of action for which diffs will be generated")
    parser.add_argument("-l", "--limit", type=int, default=-1,
                        help="Upper bound for the number of actions which will be processed")
    parser.add_argument("-s", "--size", type=int, default=300,
                        help="Size to which output data will be scaled")
    parser.add_argument("-d", "--diffs", action="store_true",
                        help="Generate diffs of performed actions instead of final image")
    ARGS = parser.parse_args()
    main()
