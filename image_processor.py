import os

from gimpfu import *


def plugin_main(directory, out):
    print directory
    filenames = [name for name in os.listdir(directory)]
    for filename in filenames:
        load_path = directory + "/" + filename
        img = pdb.gimp_file_load(load_path, load_path)
        drawable = pdb.gimp_image_get_active_drawable(img)
        pdb.plug_in_autocrop(img, drawable)
        height = drawable.height
        width = drawable.width
        if height < width:
            pdb.gimp_image_crop(img, height, height, (width-height)/2, 0)
        elif width < height:
            pdb.gimp_image_crop(img, width, width, 0, (height - width) / 2)
        new_size = 300
        pdb.gimp_image_scale(img, new_size, new_size)
        filename_without_format = filename.split(".")[0]
        file_format = filename.split(".")[1]
        if file_format == "png":
            print "PNG!"
            layer = gimp.Layer(img, "layer", new_size, new_size, RGB_IMAGE, 100, NORMAL_MODE)
            position = 1
            img.add_layer(layer, position)
            pdb.gimp_edit_fill(layer, WHITE_FILL)
            pdb.gimp_image_merge_visible_layers(img, CLIP_TO_BOTTOM_LAYER)
        save_path = out + "/" + filename_without_format + ".jpg"
        pdb.file_jpeg_save(img, pdb.gimp_image_get_active_drawable(img), save_path, save_path, 0.9, 0, 0, 0, "", 0, 0, 0, 0)


register("image_processor", "", "", "", "", "", "", "",
         [
             (PF_STRING, "path", "Path", ""),
             (PF_STRING, "out", "Out", "")
         ], [], plugin_main)

main()
