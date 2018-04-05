#!/bin/bash

cp -R ${GIMP_PROJECT}/agent/random/random_agent_plugin.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/agent/nn/nn_agent.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/nn/model/test_model_plugin.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/nn/dataset/image/image_generator_plugin.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/nn/dataset/square/square_generator_plugin.py ${GIMP_PLUGIN}
chmod -R 700 ${GIMP_PLUGIN}