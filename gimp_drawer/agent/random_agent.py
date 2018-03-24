import argparse
import os
import random

ARGS = None
RUN_PARAMETER = "RUN-NONINTERACTIVE"


def main():
    seed = ARGS.seed if ARGS.seed is not None else random.randint(0, 2 ** 32 - 1)
    run_plugin_command = "gimp {} -i -b '(python-fu-agent {} \"{}\" {} {} \"{}\" {} {})' -b '(gimp-quit 1)'"\
        .format("--verbose --debug-handlers --stack-trace-mode always" if ARGS.verbose else "",
                RUN_PARAMETER, ARGS.source, ARGS.distance, ARGS.render, ARGS.input, seed,
                ARGS.actions)
    os.system(run_plugin_command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--source", type=str, help="source image")
    parser.add_argument("--verbose", help="verbose output", action="store_true")
    parser.add_argument("--distance", type=int, help="acceptable distance", default=0)
    parser.add_argument("--render", type=int, help="render mode (0 - render \"good\" actions, 1 - no render, 2 - render everything)", default=0)
    parser.add_argument("--input", type=str, help="input image")
    parser.add_argument("--seed", type=int, help="seed (if none - random)")
    parser.add_argument("--actions", type=int, help="actions", default=999999999999999)
    ARGS = parser.parse_args()
    main()
