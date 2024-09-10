import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# Initialize the PiCamera
camera = PiCamera()

# Set camera resolution
camera.resolution = (640, 480)

# Set camera frame rate
camera.framerate = 32

# Allow the camera to warm up
time.sleep(2)

# Create a PiRGBArray object to hold image data
raw_capture = PiRGBArray(camera, size=(640, 480))

# Start capturing frames from the camera
try:
    print("Press 'q' to exit")

    # Capture continuously
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        # Convert the frame to an OpenCV image
        image = frame.array

        # Display the frame in a window
        cv2.imshow("Pi Camera", image)

        # Wait for 'q' key to stop the script
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Clear the stream for the next frame
        raw_capture.truncate(0)

finally:
    # Close the window
    cv2.destroyAllWindows()

    # Stop the camera
    camera.close()