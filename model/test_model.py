import argparse
import os

ARGS = None


def main():
    command = "gimp -i -b '(python-fu-test-model RUN-NONINTERACTIVE \"{}\" {} {} {})' -b '(gimp-quit 1)'".format(
        ARGS.model, ARGS.actions, int(ARGS.render), int(ARGS.save))
    os.system(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("model", type=str, help="path to the tested model")
    parser.add_argument("-a", "--actions", type=int, default=1000,
                        help="number of actions to perform")
    parser.add_argument("-r", "--render", help="render image during drawing", action="store_true")
    parser.add_argument("-s", "--save", help="save drawn image", action="store_true")
    ARGS = parser.parse_args()
    main()
