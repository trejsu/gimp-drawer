import argparse
import os

from src.common.plugin import Plugin

ARGS = None


def main():
    plugin = Plugin(os.path.join(os.path.expandvars('$GIMP_PROJECT'),
                    'src/nn/cnn/dataset/shape/random/random_line_generator_plugin.py'),
                    ARGS,
                    'random_line_generator')
    plugin.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--image", type=int, default=100, help="Image size")
    parser.add_argument("--number", type=int, default=5000,
                        help="Number of images for the whole dataset")
    parser.add_argument("--test", type=float, default=0.2,
                        help="Percentage of images used for testing")
    ARGS = parser.parse_args()
    main()