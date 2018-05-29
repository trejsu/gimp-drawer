import argparse
import os

from src.common.plugin import Plugin

ARGS = None


def main():
    plugin = Plugin(os.path.expandvars('$GIMP_PROJECT') + '/src/gimp/processing/scale_plugin.py',
                    ARGS, 'scale')
    plugin.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("in", type=str, help="path to directory with images to scale")
    parser.add_argument("out", type=str, help="path to directory to save results")
    parser.add_argument("size", type=int, help="target size")
    ARGS = parser.parse_args()
    main()
