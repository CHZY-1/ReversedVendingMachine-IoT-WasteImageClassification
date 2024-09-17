import time
import picamera
import sys

# image_path = '/home/pi/Pictures/captured_image.jpg'

image_path = sys.argv[1]

with picamera.PiCamera() as camera:
    
    camera.resolution = (1024, 768)
    
    time.sleep(1)
    
    camera.capture(image_path)
    
# print(image_path)