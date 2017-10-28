#!/bin/bash
#gcloud auth application-default login
for f in imagenes/*;
do python web_detect.py $f
done
