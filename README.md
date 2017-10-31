# vision_api

Uses Google Vision API to tag images using Python.
Requires your own Google API to work.

## setup
Put your images in the folder imagenes. `mv YOURPATH /PROJECTPATH/vision_api/imagenes`


## Python setup
Use `gcloud auth application-default login`to authenticate for Python.

## Run
Run `bash vision_api.sh`
The annotations will appear in your console and in the file `annotations.csv`

## Note
The script is `web_detect.py` you can manage there the number of web annotations, by default is but you can get more depending on your image.
