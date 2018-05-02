import argparse
import os

ARGS = None
COMMAND_STRING = "gimp -i -b '(python-fu-draw-triangle RUN-NONINTERACTIVE \"{}\" {} {} " \
                 "{} {} {} {} {} {} {} {} {})' -b '(gimp-quit 1)'"


def main():
    run_plugin_command = COMMAND_STRING.format(ARGS.name, ARGS.size, ARGS.r,
                                               ARGS.g, ARGS.b, ARGS.a, ARGS.x1, ARGS.y1, ARGS.x2,
                                               ARGS.y2, ARGS.x3, ARGS.y3)
    os.system(run_plugin_command)


def draw_triangle(name, size, r, g, b, a, x1, y1, x2, y2, x3, y3):
    run_plugin_command = COMMAND_STRING.format(name, size, r, g, b, a, x1, y1, x2, y2, x3, y3)
    os.system(run_plugin_command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--name", type=str, help="result name")
    parser.add_argument("--size", type=int, default=100, help="image size")
    parser.add_argument("--r", type=float, default=0., help="red part of rgba (0 - 1)")
    parser.add_argument("--g", type=float, default=0., help="green part of rgba (0 - 1)")
    parser.add_argument("--b", type=float, default=0., help="blue part of rgba (0 - 1)")
    parser.add_argument("--a", type=float, default=1., help="alpha part of rgba (0 - 1)")
    parser.add_argument("--x1", type=float, help="(0 - 1)")
    parser.add_argument("--y1", type=float, help="(0 - 1)")
    parser.add_argument("--x2", type=float, help="(0 - 1)")
    parser.add_argument("--y2", type=float, help="(0 - 1)")
    parser.add_argument("--x3", type=float, help="(0 - 1)")
    parser.add_argument("--y3", type=float, help="(0 - 1)")
    ARGS = parser.parse_args()
    main()