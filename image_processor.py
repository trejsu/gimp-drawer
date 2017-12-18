import os

from gimpfu import *


def plugin_main(directory):
    filenames = [name for name in os.listdir(directory)]
    for filename in filenames:
        load_path = directory + "/" + filename
        img = pdb.gimp_file_load(load_path, load_path)
        drawable = pdb.gimp_image_get_active_drawable(img)
        height = drawable.height
        width = drawable.width
        if height < width:
            pdb.gimp_image_crop(img, height, height, (width-height)/2, 0)
        elif width < height:
            pdb.gimp_image_crop(img, width, width, 0, (height - width) / 2)
        pdb.gimp_image_scale(img, 300, 300)
        filename_without_format = filename.split(".")[0]
        save_path = directory + "/" + filename_without_format + ".jpg"
        pdb.file_jpeg_save(img, drawable, save_path, save_path, 0.9, 0, 0, 0, "", 0, 0, 0, 0)


register("image_processor", "", "", "", "", "", "", "",
         [
             (PF_STRING, "path", "Path", "")
         ], [], plugin_main)

main()
