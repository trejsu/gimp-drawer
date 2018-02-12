import argparse
import os

ARGS = None


def main():
    os.system("gimp -i -b '(python-fu-test-model RUN-NONINTERACTIVE \"{}\" {})' -b '(gimp-quit 1)'"
              .format(ARGS.model, ARGS.test))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("model", type=str, help="path to the tested model")
    parser.add_argument("-t", "--test", type=int, default=20, help="number of tests to run")
    ARGS = parser.parse_args()
    main()
