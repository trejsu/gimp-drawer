import argparse
import os

ARGS = None


def main():
    run_plugin_command = "gimp {} -i -b '(python-fu-nn-agent RUN-NONINTERACTIVE \"{}\" {} {} " \
                         "\"{}\" {} {} {} {} {})' -b '(gimp-quit 1)'"\
        .format("--verbose --debug-handlers --stack-trace-mode always" if ARGS.verbose else "",
                ARGS.source, int(ARGS.render), ARGS.actions, ARGS.model, int(ARGS.save), ARGS.size,
                ARGS.channels, int(ARGS.sigmoid), ARGS.sleep)
    print(run_plugin_command)
    os.system(run_plugin_command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--source", type=str)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--render", action="store_true", help="render image during drawing")
    parser.add_argument("--actions", default=1000, type=int, help="number of shapes to draw")
    parser.add_argument("--model", type=str)
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--size", type=int, default=100,
                        help="size of result image - must match network input")
    parser.add_argument("--channels", type=int, default=3)
    parser.add_argument("--sigmoid", action="store_true", help="apply sigmoid to generated args")
    parser.add_argument("--sleep", type=int, default=1,
                        help="second to pause after rendering action")
    ARGS = parser.parse_args()
    main()
