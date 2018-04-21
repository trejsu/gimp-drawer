import argparse
import os

ARGS = None
COMMAND_STRING = "gimp -i -b '(python-fu-draw-rectangle RUN-NONINTERACTIVE \"{}\" {} {} {} {} " \
            "{} {} {} {} {} {})' -b '(gimp-quit 1)'"


def main():
    run_plugin_command = COMMAND_STRING.format(ARGS.name, ARGS.size, ARGS.r, ARGS.g, ARGS.b,
                                               ARGS.a, ARGS.x, ARGS.y, ARGS.w, ARGS.h, ARGS.rotation)
    os.system(run_plugin_command)


def draw_rectangle(name, x, y, w, h, size=100, r=0., g=0., b=0., a=1., rotation=0.5):
    run_plugin_command = COMMAND_STRING.format(name, size, r, g, b, a, x, y, w, h, rotation)
    os.system(run_plugin_command)


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
    ARGS = parser.parse_args()
    main()