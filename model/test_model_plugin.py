import os
import tqdm

from model.conv_network import ConvNetwork
from gimpfu import *
from model.dataset.data_set import DataSet


def plugin_main(model_path, actions_number):
    data = DataSet()
    test_mse(data, model_path)
    test_whole_images(data, model_path, actions_number)


def test_whole_images(data, model_path, actions_number):
    images_dir = os.path.expandvars("$GIMP_PROJECT/resources/scaled_images/")
    print "Train image test"
    label = data.train.random_label()
    image_path = images_dir + str(label[0]) + ".jpg"
    pdb.python_fu_conv_agent(image_path, 0, "None", actions_number, model_path)
    print "Test image test"
    label = data.test.random_label()
    image_path = images_dir + str(label[0]) + ".jpg"
    pdb.python_fu_conv_agent(image_path, 0, "None", actions_number, model_path)


def test_mse(data, model_path):
    conv_network = ConvNetwork(model_path)
    for _ in tqdm.tqdm(range(data.test.batch_n)):
        x, y, label = data.test.next_batch()
        tqdm.tqdm.write("mse: %g" % conv_network.eval_error(x, y))


register("test_model", "", "", "", "", "", "", "",
         [
             (PF_STRING, "model_path", "path to the tested model", ""),
             (PF_INT, "actions_number", "number of actions to perform", 1000)
         ], [], plugin_main)

main()
