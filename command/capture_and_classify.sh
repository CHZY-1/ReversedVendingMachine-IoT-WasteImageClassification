#!/bin/bash

source /home/pi/Desktop/waste_classification/activate_env.sh

# timestammp=$(date +"%Y%m%d_%H%M%S")
# image_path="/home/pi/Pictures/captured_image_$timestamp.jpg"
image_path='/home/pi/Pictures/captured_image.jpg'


python3 /home/pi/Desktop/waste_classification/RaspberryPi-WasteImageClassification/camera_capture.py "$image_path"


# classification_output=$(python3 /home/pi/Desktop/waste_classification/RaspberryPi-WasteImageClassification/classify_image.py "$image_path")
echo "image_path: $image_path"
# echo "$classification_output"

python3 /home/pi/Desktop/waste_classification/RaspberryPi-WasteImageClassification/classify_image.py "$image_path"



