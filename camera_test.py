from picamera import PiCamera
from time import sleep

def test_camera():
    try:
        camera = PiCamera()
        camera.start_preview()
        sleep(5)
        camera.capture('/home/pi/test_image.jpg')
        camera.stop_preview()
        print("Camera test successful. Image saved as test_image.jpg")
    except Exception as e:
        print(f"Camera test failed: {str(e)}")
    finally:
        camera.close()

if __name__ == "__main__":
    test_camera()