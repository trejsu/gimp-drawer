import argparse
import os
from src.common.plugin import Plugin

ARGS = None


def main():
    plugin = Plugin(os.path.expandvars('$GIMP_PROJECT') +
                    '/src/nn/cnn/dataset/shape/random/random_shape_generator_plugin.py', ARGS,
                    'random_shape_generator')
    plugin.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--image", type=int, default=100, help="Image size")
    parser.add_argument("--number", type=int, default=10000,
                        help="Number of images for the whole dataset")
    parser.add_argument("--max_examples_per_part", type=int, default=3000,
                        help="Max images in one dataset file")
    parser.add_argument("--test", type=float, default=0.2,
                        help="Percentage of images used for testing")
    parser.add_argument("--without_rotation", action="store_true")
    ARGS = parser.parse_args()
    main()