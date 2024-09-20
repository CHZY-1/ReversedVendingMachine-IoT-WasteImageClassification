import RPi.GPIO as GPIO
import time

# Suppress warnings
GPIO.setwarnings(False)

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for buttons
BUTTON_CONTINUE = 5
BUTTON_STOP = 6

# Setup GPIO
GPIO.setup(BUTTON_CONTINUE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_pressed_callback(channel):
    if channel == BUTTON_CONTINUE:
        print("Continue button pressed!")
    elif channel == BUTTON_STOP:
        print("Stop button pressed!")

# Add event detection for both buttons
GPIO.add_event_detect(BUTTON_CONTINUE, GPIO.FALLING, callback=button_pressed_callback, bouncetime=300)
GPIO.add_event_detect(BUTTON_STOP, GPIO.FALLING, callback=button_pressed_callback, bouncetime=300)

print("Button test program running. Press CTRL+C to exit.")
print("Press the Continue or Stop button to see the output.")

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram stopped by user")

finally:
    GPIO.cleanup()