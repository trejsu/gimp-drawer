#!/bin/bash

cp -R ${GIMP_PROJECT}/src/nn/dataset/shape/square_with_parameters_generator_plugin.py "${GIMP_PLUGIN}"
cp -R ${GIMP_PROJECT}/src/gimp/draw/draw_selection_shape_plugin.py "${GIMP_PLUGIN}"
cp -R ${GIMP_PROJECT}/src/gimp/draw/draw_triangle_plugin.py "${GIMP_PLUGIN}"
cp -R ${GIMP_PROJECT}/src/gimp/draw/draw_line_plugin.py "${GIMP_PLUGIN}"
cp -R ${GIMP_PROJECT}/src/agent/nn/nn_agent_plugin.py "${GIMP_PLUGIN}"
cp -R ${GIMP_PROJECT}/src/nn/dataset/shape/random/random_selection_shape_generator_plugin.py "${GIMP_PLUGIN}"
cp -R ${GIMP_PROJECT}/src/nn/dataset/shape/random/random_triangle_generator_plugin.py "${GIMP_PLUGIN}"
cp -R ${GIMP_PROJECT}/src/nn/dataset/shape/random/random_line_generator_plugin.py "${GIMP_PLUGIN}"
chmod -R 700 "${GIMP_PLUGIN}"