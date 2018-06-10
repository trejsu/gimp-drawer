import argparse
import os

from src.common.plugin import Plugin

ARGS = None


def main():
    plugin = Plugin(os.path.expandvars('$GIMP_PROJECT') +
                    '/src/gimp/draw/generate_actions_plugin.py', ARGS, 'generate_actions')
    plugin.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--output_path", type=str)
    parser.add_argument("--image", type=str)
    parser.add_argument("--actions", type=int)
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--size", type=int)
    ARGS = parser.parse_args()
    main()
