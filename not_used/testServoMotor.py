import RPi.GPIO as GPIO
import time

# Suppress warnings
GPIO.setwarnings(False)

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
SERVO_SORT_PIN = 18
SERVO_COIN_PIN = 19

# Setup GPIO
GPIO.setup(SERVO_SORT_PIN, GPIO.OUT)
GPIO.setup(SERVO_COIN_PIN, GPIO.OUT)

# Initialize PWM on both pins to 50Hz
servo_sort = GPIO.PWM(SERVO_SORT_PIN, 50)
servo_coin = GPIO.PWM(SERVO_COIN_PIN, 50)

# Start PWM running, with value of 0 (pulse off)
servo_sort.start(0)
servo_coin.start(0)

def set_angle(servo, angle):
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

def initialize_servo(servo, name):
    print(f"Initializing {name} servo...")
    set_angle(servo, 0)
    time.sleep(1)
    print(f"{name} servo initialized to 0 degrees.")

def test_servo(servo, name):
    print(f"Testing {name} servo")
    for angle in range(0, 181, 30):  # Test from 0 to 180 degrees in 30-degree increments
        print(f"Moving to {angle} degrees")
        set_angle(servo, angle)
        time.sleep(1)
    set_angle(servo, 90)  # Return to middle position
    print(f"{name} servo test complete")

def main():
    try:
        initialize_servo(servo_sort, "Sorting")
        initialize_servo(servo_coin, "Coin dispensing")
        
        while True:
            choice = input("Enter 's' to test sorting servo, 'c' to test coin servo, 'q' to quit, or an angle (0-180): ")
            if choice.lower() == 's':
                test_servo(servo_sort, "Sorting")
            elif choice.lower() == 'c':
                test_servo(servo_coin, "Coin dispensing")
            elif choice.lower() == 'q':
                break
            elif choice.isdigit() and 0 <= int(choice) <= 180:
                angle = int(choice)
                servo_choice = input("Which servo? (s for sorting, c for coin): ")
                if servo_choice.lower() == 's':
                    set_angle(servo_sort, angle)
                    print(f"Sorting servo moved to {angle} degrees")
                elif servo_choice.lower() == 'c':
                    set_angle(servo_coin, angle)
                    print(f"Coin servo moved to {angle} degrees")
                else:
                    print("Invalid servo choice")
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        servo_sort.stop()
        servo_coin.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()