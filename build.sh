#!/bin/bash

cp -R ${GIMP_PROJECT}/gimp_drawer/agent/random_agent.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/gimp_drawer/agent/conv_agent.py ${GIMP_PLUGIN}
#cp -R ${GIMP_PROJECT}/gimp_drawer/generator/image_generator.py ${GIMP_PLUGIN}
chmod -R 700 ${GIMP_PLUGIN}