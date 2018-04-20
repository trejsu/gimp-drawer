import os
import tqdm


from src.nn.model.conv_network import ConvNetwork
from gimpfu import *
from src.nn.dataset.image.image_dataset import ImageDataset


def plugin_main(model_path, actions_number, render, save, train, examples, size):
    data = ImageDataset()
    conv_network = ConvNetwork(model_path)
    test_mse(data, conv_network, examples if examples is not None else data.test.batch_n, "Testing test set mse")
    if train:
        test_mse(data, conv_network, examples if examples is not None else data.train.batch_n, "Testing train set mse")
    test_whole_images(data, model_path, actions_number, render, save, size)


def test_whole_images(data, model_path, actions_number, render, save, size):
    images_dir = os.path.expandvars("$GIMP_PROJECT/resources/scaled_images/")
    print "Train image test"
    label = data.train.random_label()
    print "Testing image", label
    image_path = images_dir + str(label[0]) + ".jpg"
    pdb.python_fu_conv_agent(image_path, render, "None", actions_number, model_path, save, size)
    print "Test image test"
    label = data.test.random_label()
    print "Testing image", label
    image_path = images_dir + str(label[0]) + ".jpg"
    pdb.python_fu_conv_agent(image_path, render, "None", actions_number, model_path, save, size)


def test_mse(data, conv_network, examples, message):
    # mse = np.zeros((1, examples))
    for i in tqdm.tqdm(range(examples), message):
        x, y, label = data.test.next_batch()
        err = conv_network.eval_error(x, y)
        # mse[i] = err
        tqdm.tqdm.write("mse: %g" % err)
    # return np.average(mse)


register("test_model", "", "", "", "", "", "", "",
         [
             (PF_STRING, "model_path", "path to the tested model", ""),
             (PF_INT, "actions_number", "number of actions to perform", 1000),
             (PF_BOOL, "render", "render image during drawing", True),
             (PF_BOOL, "save", "save drawn image", False),
             (PF_BOOL, "train", "include mse testing for train set", False),
             (PF_INT, "examples", "number of batches for mse testing - whole set when argument missing", False),
             (PF_INT, "size", "Size of drawn image", 100)
         ], [], plugin_main)

main()