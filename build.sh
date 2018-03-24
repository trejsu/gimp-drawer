#!/bin/bash

cp -R ${GIMP_PROJECT}/gimp_drawer/agent/random_agent_plugin.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/gimp_drawer/agent/conv_agent.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/model/test_model_plugin.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/model/dataset/image_generator_plugin.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/model/square/square_generator_plugin.py ${GIMP_PLUGIN}
chmod -R 700 ${GIMP_PLUGIN}