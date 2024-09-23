import picamera
import time
import os
from datetime import datetime
import RPi.GPIO as GPIO

# Set up GPIO
LED_PIN = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

def capture_images(output_folder, num_images=10, delay=2):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with picamera.PiCamera() as camera:
        # Camera warm-up time
        print("Warming up the camera...")
        time.sleep(2)

        # Set camera resolution (you can adjust this as needed)
        camera.resolution = (640, 480)

        for i in range(num_images):
            # Turn on the LED
            GPIO.output(LED_PIN, GPIO.HIGH)

            # Generate a unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}_{i+1}.jpg"
            filepath = os.path.join(output_folder, filename)

            # Capture the image
            print(f"Capturing image {i+1}/{num_images}...")
            camera.capture(filepath)
            print(f"Saved: {filepath}")

            # Wait before the next capture
            if i < num_images - 1:
                print(f"Waiting {delay} seconds before next capture...")
                time.sleep(delay)

     # Turn off the LED
    GPIO.output(LED_PIN, GPIO.LOW)
    print("Image capture complete!")

def cleanup():
    GPIO.cleanup()
    print("GPIO cleaned up")

if __name__ == "__main__":
    # Set your desired output folder
    output_folder = "/home/pi/Desktop/waste_classification/RaspberryPi-WasteImageClassification/trainingData/plasticNoWindow"

    # Set the number of images you want to capture
    num_images = 4

    # Set the delay between captures (in seconds)
    delay_between_captures = 1

    try:
        capture_images(output_folder, num_images, delay_between_captures)
    finally:
        cleanup()