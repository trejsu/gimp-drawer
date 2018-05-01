#!/bin/bash

cp -R ${GIMP_PROJECT}/src/nn/dataset/shape/square_with_parameters_generator_plugin.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/src/gimp/draw_rectangle_plugin.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/src/agent/nn/nn_agent_plugin.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/src/nn/dataset/shape/random/random_selection_shape_generator_plugin.py ${GIMP_PLUGIN}
chmod -R 700 ${GIMP_PLUGIN}