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
        
        # Allow time for the camera to warm up
        time.sleep(2)
        
        print("Press 'q' to quit the stream")
        
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
                    
                    # Check for 'q' key press to quit
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            
            finally:
                # Clean up
                cv2.destroyAllWindows()
                print("Stream ended")

if __name__ == "__main__":
    main()