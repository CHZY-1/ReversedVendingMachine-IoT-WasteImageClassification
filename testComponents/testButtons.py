import RPi.GPIO as GPIO
import time

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins connected to the buttons
BUTTON_PINS = [5, 6]

# Set up the button pins as inputs with pull-up resistors
for pin in BUTTON_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_button_states():
    states = {}
    for pin in BUTTON_PINS:
        # Read the state of the button (0 if pressed, 1 if not pressed due to pull-up)
        state = GPIO.input(pin)
        # Convert to more intuitive representation (True if pressed, False if not pressed)
        states[pin] = not state
    return states

try:
    print("Press Ctrl+C to exit")
    while True:
        button_states = read_button_states()
        
        # Print the state of each button
        for pin, is_pressed in button_states.items():
            state_str = "Pressed" if is_pressed else "Not pressed"
            print(f"Button on GPIO {pin}: {state_str}")
        
        print("-" * 20)  # Separator for readability
        
        time.sleep(1)  # Short delay to avoid excessive CPU usage

except KeyboardInterrupt:
    print("\nProgram stopped by user")
finally:
    GPIO.cleanup()  # Clean up GPIO on program exit