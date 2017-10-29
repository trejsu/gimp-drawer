#!/usr/bin/python

import time
import os
import datetime
import numpy

from gimpfu import *
from scipy import sum

OUT_PATH = None


def plugin_main(infile, iterations, metric):
    start = time.time()
    execute_loop(infile, iterations, metric)
    end = time.time()
    total = end - start
    print "Plugin executed in", "{:1.0f}".format(total / 60), "minutes and", \
        "{:1.0f}".format(total % 60), "seconds."


def execute_loop(infile, iterations, metric):
    src_img = load_file(infile)
    display_image(src_img)
    src_array = read(src_img)
    actual_img = new_image(get_width(src_img), get_height(src_img))
    save_iteration(actual_img, 0)

    for i in range(1, iterations + 1):
        print "iteration", i
        actual_array = read(actual_img)
        # todo: refactor resolve metric
        actual_diff = compare_images(src_array, actual_array, resolve_metric(metric))
        while True:
            new_img = pdb.gimp_image_duplicate(actual_img)
            pdb.python_fu_perform_random_action(new_img)
            new_array = read(new_img)
            new_diff = compare_images(src_array, new_array, resolve_metric(metric))
            if new_diff < actual_diff:
                pdb.gimp_displays_reconnect(actual_img, new_img)
                save_iteration(new_img, i)
                actual_img = new_img
                break
            close(new_img)


def load_file(filename):
    return pdb.gimp_file_load(filename, filename)


def open_iteration(i):
    return load_file(get_path_of_iteration(i))


def new_image(width, height):
    image_id = gimp.Image(width, height, RGB_IMAGE)
    layer = gimp.Layer(image_id, "name", width, height, RGB_IMAGE, 100, NORMAL_MODE)
    image_id.add_layer(layer, 0)
    display_image(image_id)
    pdb.gimp_edit_fill(layer, BACKGROUND_FILL)
    return image_id


def display_image(image_id):
    gimp.Display(image_id)
    gimp.displays_flush()


def get_width(image):
    return get_drawable(image).width


def get_drawable(image):
    return pdb.gimp_image_active_drawable(image)


def get_height(image):
    return pdb.gimp_image_active_drawable(image).height


def save_iteration(image, i):
    global OUT_PATH
    if OUT_PATH is None:
        date = datetime.datetime.now()
        OUT_PATH = os.path.expandvars("$GIMP_PROJECT/out/%s" % date.isoformat())
        os.mkdir(OUT_PATH)
    filename = get_path_of_iteration(i)
    pdb.file_jpeg_save(image, get_drawable(image), filename, filename,
                       0.9, 0, 0, 0, "", 0, 0, 0, 0)


def read(image):
    drawable = get_drawable(image)
    width = drawable.width
    height = drawable.height
    bpp = drawable.bpp
    pixel_region = drawable.get_pixel_rgn(0, 0, width, height, False)
    array = numpy.fromstring(pixel_region[:, :], "B")
    assert array.size == width * height * bpp
    image = numpy.array(array.reshape(height, width, bpp), "d")[:, :, 0:min(bpp, 3)]
    return image / 256.0


def compare_images(img1, img2, calculate_distance):
    return calculate_distance(img1 - img2)


def get_path_of_iteration(i):
    return "%s/iteration_%s.jpg" % (OUT_PATH, i)


def resolve_metric(metric):
    if metric == "L1":
        return lambda diff: sum(abs(diff))
    elif metric == "L2":
        return lambda diff: math.sqrt(sum(diff ** 2))


def close(image):
    gimp.delete(image)


register("correct_image", "", "", "", "", "", "", "",
         [
             (PF_STRING, "infile", "File", ""),
             (PF_INT, "iterations", "Number of iterations", 100),
             (PF_STRING, "metric", "Metric", "")
         ],
         [],
         plugin_main)

main()
