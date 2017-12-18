#!/bin/bash

cp -R ${GIMP_PROJECT}/gimp_drawer/agent/agent.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/gimp_drawer/agent/image_generator.py ${GIMP_PLUGIN}
cp -R ${GIMP_PROJECT}/image_processor.py ${GIMP_PLUGIN}
chmod -R 700 ${GIMP_PLUGIN}