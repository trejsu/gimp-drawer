import argparse
import os

ARGS = None


def main():
    run_plugin_command = "gimp -i -b '(python-fu-square-generator RUN-NONINTERACTIVE {} {} {} {})'"\
                         " -b '(gimp-quit 1)'"\
                        .format(ARGS.image, ARGS.square, ARGS.number, ARGS.test)
    os.system(run_plugin_command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--image", type=int, default=100, help="Image size")
    parser.add_argument("--square", type=int, default=20, help="Square size")
    parser.add_argument("--number", type=int, default=5000,
                        help="Number of images for the whole dataset")
    parser.add_argument("--test", type=float, default=0.3,
                        help="Percentage of images used for testing")
    ARGS = parser.parse_args()
    main()