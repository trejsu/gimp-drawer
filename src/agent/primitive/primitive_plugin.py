from gimpfu import *
from src.agent.primitive.env import Environment


def plugin_main(input_img, output_img, background, alpha, output_size, mode, verbose, nth, shapes,
                render_mode):
    env = Environment(input_path=input_img, output_path=output_img, output_size=output_size,
                      bg=background)
    env.save()

