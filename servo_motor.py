import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self, pin, freq=50, min_angle=0, max_angle=180):
        self.pin = pin
        self.freq = freq
        self.min_angle = min_angle
        self.max_angle = max_angle
        
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.pwm.start(0)

    def angle_to_duty_cycle(self, angle):
        return (angle / 18) + 2

    def rotate(self, angle):
        if angle < self.min_angle or angle > self.max_angle:
            print(f"Warning: Attempted to move servo to {angle} degrees, which is out of range.")
            return False
        
        duty = self.angle_to_duty_cycle(angle)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.3)  # Allow time for the servo to reach the position
        self.pwm.ChangeDutyCycle(0)  # Stop the PWM signal
        return True

    def cleanup(self):
        self.pwm.stop()

class SortingServo(ServoMotor):
    def __init__(self, pin, initial_angle=90):
        super().__init__(pin, min_angle=0, max_angle=180)
        self.initial_angle = initial_angle
        self.rotate(self.initial_angle)  # Set to initial position on startup
    
    def sort(self, target_angle):
        self.rotate(target_angle)  # Move to sorting position
        time.sleep(1)  # Wait for material to be sorted
        self.rotate(self.initial_angle)  # Return to initial position
        return True

    def sort_plastic(self):
        return self.sort(130)
    
    def sort_metal(self):
        return self.sort(50)

class CoinDispenserServo(ServoMotor):
    def __init__(self, pin):
        super().__init__(pin, min_angle=0, max_angle=180)
    
    def dispense_coin(self):
        self.rotate(90)
        time.sleep(0.5)
        self.rotate(0)
        return True

def setup_servos(sort_pin, coin_pin):
    return SortingServo(sort_pin), CoinDispenserServo(coin_pin)