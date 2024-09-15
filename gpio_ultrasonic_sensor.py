import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
TRIG_PIN = 23  # GPIO pin
ECHO_PIN = 24  # GPIO pin

# Set up the GPIO pins
GPIO.setup(TRIG_PIN, GPIO.OUT)  # Set TRIG as an output
GPIO.setup(ECHO_PIN, GPIO.IN)   # Set ECHO as an input

# Function to measure the distance
def measure_distance():
    # Ensure the TRIG pin is low
    GPIO.output(TRIG_PIN, False)
    time.sleep(2)  # Let the sensor settle for 2 seconds

    # Trigger the ultrasonic burst
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)  # 10 microseconds pulse
    GPIO.output(TRIG_PIN, False)

    # Wait for the ECHO pin to go HIGH (start of the pulse)
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    # Wait for the ECHO pin to go LOW (end of the pulse)
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate the pulse duration
    pulse_duration = pulse_end - pulse_start

    # Calculate the distance (Speed of sound = 34300 cm/s)
    distance = pulse_duration * 17150  # distance in cm

    # Round the distance to 2 decimal places
    distance = round(distance, 2)

    return distance

try:
    while True:
        dist = measure_distance()
        print(f"Distance: {dist} cm")
        time.sleep(1)  # Wait for 1 second before the next reading

except KeyboardInterrupt:
    print("Measurement stopped by user")

finally:
    # Clean up the GPIO pins before exiting
    GPIO.cleanup()