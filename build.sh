#!/bin/bash

cp -R ${GIMP_PROJECT}/src/nn/dataset/square/square_with_parameters_generator_plugin.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/src/gimp/draw_rectangle_plugin.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/src/agent/nn/nn_agent_plugin.py ${GIMP_PLUGIN}
chmod -R 700 ${GIMP_PLUGIN}