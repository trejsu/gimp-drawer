import argparse
import os

ARGS = None


def main():
    os.system("gimp -i -b '(python-fu-test-model RUN-NONINTERACTIVE \"{}\" {})' -b '(gimp-quit 1)'"
              .format(ARGS.model, ARGS.actions))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("model", type=str, help="path to the tested model")
    parser.add_argument("-a", "--actions", type=int, default=1000,
                        help="number of actions to perform")
    ARGS = parser.parse_args()
    main()
