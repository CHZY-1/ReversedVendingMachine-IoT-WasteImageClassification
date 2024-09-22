import cv2
import picamera
import picamera.array
import time

def main():
    # Initialize the camera
    with picamera.PiCamera() as camera:
        # Set up the camera
        camera.resolution = (640, 480)
        camera.framerate = 24
        
        # Set zoom to capture a wider view
        # The zoom is set as (x, y, w, h) where each value is between 0.0 and 1.0
        # (0.0, 0.0, 1.0, 1.0) is the full field of view
        camera.zoom = (0.0, 0.0, 1.0, 1.0)
        
        # You can also adjust the field of view using sensor mode
        # camera.sensor_mode = 2  # Use a wider field of view mode
        
        # Allow time for the camera to warm up
        time.sleep(2)
        
        print("Press 'q' to quit the stream")
        print("Press 'w' to zoom out, 'e' to zoom in")
        
        # Create a window
        cv2.namedWindow("Pi Camera Live Stream", cv2.WINDOW_NORMAL)
        
        # Use PiRGBArray to get frames from the camera
        with picamera.array.PiRGBArray(camera, size=(640, 480)) as output:
            try:
                for _ in camera.capture_continuous(output, format="bgr", use_video_port=True):
                    # Get the frame
                    frame = output.array
                    
                    # Display the frame
                    cv2.imshow("Pi Camera Live Stream", frame)
                    
                    # Clear the stream for the next frame
                    output.truncate(0)
                    
                    # Check for key presses
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    elif key == ord('w'):
                        # Zoom out
                        x, y, w, h = camera.zoom
                        camera.zoom = (max(0.0, x-0.1), max(0.0, y-0.1), min(1.0, w+0.2), min(1.0, h+0.2))
                        print(f"Zoomed out: {camera.zoom}")
                    elif key == ord('e'):
                        # Zoom in
                        x, y, w, h = camera.zoom
                        camera.zoom = (min(0.9, x+0.1), min(0.9, y+0.1), max(0.1, w-0.2), max(0.1, h-0.2))
                        print(f"Zoomed in: {camera.zoom}")
            
            finally:
                # Clean up
                cv2.destroyAllWindows()
                print("Stream ended")

if __name__ == "__main__":
    main()