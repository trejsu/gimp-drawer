import argparse
import os

from src.common.plugin import Plugin

ARGS = None


def main():
    plugin = Plugin(os.path.expandvars('$GIMP_PROJECT') +
                    '/src/gimp/draw/draw_selection_shape_plugin.py', ARGS, 'draw_selection_shape')
    plugin.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--name", type=str, help="result name")
    parser.add_argument("--size", type=int, default=100, help="image size")
    parser.add_argument("--r", type=float, default=0., help="red part of rgba (0 - 1)")
    parser.add_argument("--g", type=float, default=0., help="green part of rgba (0 - 1)")
    parser.add_argument("--b", type=float, default=0., help="blue part of rgba (0 - 1)")
    parser.add_argument("--a", type=float, default=1., help="alpha part of rgba (0 - 1)")
    parser.add_argument("--x", type=float, help="x coordinate of left upper corner (0 - 1)")
    parser.add_argument("--y", type=float, help="y coordinate of left upper corner (0 - 1)")
    parser.add_argument("--w", type=float, help="rectangle width (0 - 1)")
    parser.add_argument("--h", type=float, help="rectangle height (0 - 1)")
    parser.add_argument("--rotation", type=float, default=0.5,
                        help="rectangle rotation (0 - 1) - 0 means -180 rotation, 0.5 - 0, 1 - 180")
    parser.add_argument("--shape", type=str, choices=["rectangle", "ellipse"])
    ARGS = parser.parse_args()
    main()
