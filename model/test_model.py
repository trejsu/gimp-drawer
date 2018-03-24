import argparse
import os

ARGS = None


def main():
    command = "gimp -i -b '(python-fu-test-model RUN-NONINTERACTIVE \"{}\" {} {} {} {} {})' -b '(gimp-quit 1)'".format(
        ARGS.model, ARGS.actions, int(ARGS.render), int(ARGS.save), int(ARGS.train), ARGS.examples, ARGS.size)
    os.system(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("model", type=str, help="path to the tested model")
    parser.add_argument("--actions", type=int, default=1000,
                        help="number of actions to perform")
    parser.add_argument("--render", help="render image during drawing", action="store_true")
    parser.add_argument("--save", help="save drawn image", action="store_true")
    parser.add_argument("--train", help="include mse testing for train set", action="store_true")
    parser.add_argument("--examples", type=int,
                        help="number of batches for mse testing - whole set when argument missing")
    parser.add_argument("--size", type=int, default=100, help="image size")
    ARGS = parser.parse_args()
    main()
