import argparse
import os

from src.common.plugin import Plugin
from src.common.config import PROJECT_BASE_PATH

ARGS = None
PLUGIN_PATH = 'src/agent/primitive/primitive_plugin.py'


def main():
    plugin = Plugin(plugin_file=os.path.join(PROJECT_BASE_PATH, PLUGIN_PATH), args=ARGS,
                    plugin_name='primitive')
    plugin.run()


def validate_args():
    if ARGS.shapes < 1:
        raise argparse.ArgumentTypeError("min number of shapes is 1")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input-img", type=str, help="input image path", required=True)
    parser.add_argument("--output-img", type=str, help="output image path", required=True)
    parser.add_argument("--background", type=str, help="background color (hex)", default="None")
    parser.add_argument("--alpha", type=int, help="alpha value", default=128)
    parser.add_argument("--output-size", type=int, help="output image size", default=1024)
    parser.add_argument("--mode", type=int, help="drawing mode",
                        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8], default=1)
    parser.add_argument("--workers", type=int,
                        help="number of parallel workers (all cores by default)", default=0)
    parser.add_argument("--verbose", help="verbose output", action="store_true")
    parser.add_argument('--nth', type=int, help="save every nth frame (put %d in path)", default=1)
    parser.add_argument('--shapes', type=int, help="number of shapes to draw",
                        required=True)
    ARGS = parser.parse_args()
    validate_args()
    main()
