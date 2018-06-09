import argparse
import os

ARGS = None


def main():
    run_plugin_command = "gimp -i -b '(python-fu-random-selection-shape-with-parameters-generator " \
                         "RUN-NONINTERACTIVE {} {} {} \"{}\")' -b '(gimp-quit 1)'"\
        .format(ARGS.image, ARGS.number, ARGS.test, ARGS.shape)
    os.system(run_plugin_command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--image", type=int, default=100, help="Image size")
    parser.add_argument("--number", type=int, default=5000,
                        help="Number of images for the whole dataset")
    parser.add_argument("--test", type=float, default=0.2,
                        help="Percentage of images used for testing")
    parser.add_argument("--shape", type=str, choices=["rectangle", "ellipse"])
    ARGS = parser.parse_args()
    main()