import os

from gimpfu import *
import tqdm


def plugin_main(path_in, path_out, size):
    filenames = os.listdir(path_in)
    for filename in tqdm.tqdm(filenames):
        load_path = path_in + "/" + filename
        img = pdb.gimp_file_load(load_path, load_path)
        pdb.gimp_image_scale(img, size, size)
        save_path = path_out + "/" + filename
        pdb.file_jpeg_save(img, pdb.gimp_image_get_active_drawable(img), save_path, save_path, 0.9,
                           0, 0, 0, "", 0, 0, 0, 0)
        pdb.gimp_image_delete(img)
