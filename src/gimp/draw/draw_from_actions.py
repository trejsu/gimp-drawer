import argparse
import os

from src.common.plugin import Plugin

ARGS = None


def main():
    plugin = Plugin(os.path.expandvars('$GIMP_PROJECT') +
                    '/src/gimp/draw/draw_from_actions_plugin.py', ARGS, 'draw_from_actions')
    plugin.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--action_args", type=str)
    parser.add_argument("--size", type=int)
    parser.add_argument("--output_path", type=str)
    ARGS = parser.parse_args()
    main()
