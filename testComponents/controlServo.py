import RPi.GPIO as GPIO
import time

class ServoController:
    def __init__(self, pin, freq=50, min_angle=0, max_angle=180):
        self.pin = pin
        self.freq = freq
        self.min_angle = min_angle
        self.max_angle = max_angle
#        self.current_angle = 90  # Start Position for sorting servo
        self.current_angle = 110 # Start Position for coin dispenser Servo
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.pwm.start(0)
        self.rotate_to(self.current_angle)  # Move to initial position
        
    def angle_to_duty_cycle(self, angle):
        return (angle / 18) + 2
    
    def rotate_to(self, angle):
        if angle < self.min_angle or angle > self.max_angle:
            print(f"Error: Angle must be between {self.min_angle} and {self.max_angle}")
            return
        
        duty = self.angle_to_duty_cycle(angle)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(2.5)  # Allow time for the servo to reach the position
        self.pwm.ChangeDutyCycle(0)  # Stop the PWM signal
        self.current_angle = angle
    
    def rotate_by(self, degrees):
        new_angle = self.current_angle + degrees
        self.rotate_to(max(self.min_angle, min(self.max_angle, new_angle)))
    
    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

def main():
#    servo_pin = 18  # Sorting Testing Port    
    servo_pin = 19  # Coin Dispenser Testing Port
    servo = ServoController(servo_pin)
    
    print("Bidirectional Servo Motor Control Program")
    print("Enter a number to rotate by that many degrees")
    print("Positive numbers rotate clockwise, negative counterclockwise")
    print("Enter 'q' to quit")
    
    try:
        while True:
            user_input = input(f"Current angle: {servo.current_angle}. Enter degrees to rotate: ")
            
            if user_input.lower() == 'q':
                break
            
            try:
                degrees = int(user_input)
                servo.rotate_by(degrees)
                print(f"Rotated by {degrees} degrees. New angle: {servo.current_angle}")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    
    finally:
        servo.cleanup()
        print("GPIO cleaned up")

if __name__ == "__main__":
    main()