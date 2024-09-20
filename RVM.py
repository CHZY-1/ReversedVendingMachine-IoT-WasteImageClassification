import RPi.GPIO as GPIO
import time
import os
import I2C_LCD_driver
from picamera import PiCamera
from WasteClassifier import WasteClassifier
from UltrasonicSensorPublish import UltrasonicSensorPublisher
from MQTTManager import MQTTManager
from servo_motor import setup_servos

mqtt_manager = MQTTManager(broker_address="RVMPi.local")
# mqtt_manager.connect()

# Suppress Warnings
GPIO.setwarnings(False)

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Sensor pins
IR_SENSOR_PIN = 16  # FC-51 Motion Sensor
BUTTON_CONTINUE = 5
BUTTON_STOP = 6

# Actuator pins
LED_PIN = 12
BUZZER_PIN = 13
SERVO_SORT_PIN = 18
SERVO_COIN_PIN = 19

# Setup GPIO
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)
GPIO.setup(BUTTON_CONTINUE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Initialize servo motors
servo_sort, servo_coin = setup_servos(SERVO_SORT_PIN, SERVO_COIN_PIN)

# LCD initialization
lcd = I2C_LCD_driver.I2C_LCD_driver()

# Initialize WasteClassifier
model_path = "/home/pi/Desktop/waste_classification/RaspberryPi-WasteImageClassification/model/model.tflite"
waste_classifier = WasteClassifier(mqtt_manager, model_path)

# Initialize UltrasonicSensorPublisher
ULTRASONIC_SENSORS = [
    {"trigger": 23, "echo": 24},  # Left sensor
    {"trigger": 27, "echo": 22},  # Right sensor
]
ultrasonic_publisher = UltrasonicSensorPublisher(ULTRASONIC_SENSORS, mqtt_manager)

def capture_image(image_path):
    """Capture an image using the Raspberry Pi camera."""
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.start_preview()
    time.sleep(2)  # Allow the camera to warm up
    camera.capture(image_path)
    camera.stop_preview()
    camera.close()

def user_prompt():
    """Prompt the user to continue or cash out."""
    lcd.lcd_clear()
    lcd.lcd_display_string("1: Continue", 1)
    lcd.lcd_display_string("2: Cash Out", 2)
    while True:
        if GPIO.input(BUTTON_CONTINUE):
            time.sleep(0.2)
            return "continue"
        if GPIO.input(BUTTON_STOP):
            time.sleep(0.2)
            return "stop"
        time.sleep(0.1)

def dispense_coins(count):
    """Dispense coins based on the material count."""
    for _ in range(count):
        servo_coin.dispense_coin()
        time.sleep(1)

def main():
    material_count = 0
    mqtt_manager.connect()
    ultrasonic_publisher.publish_sensor_data()
    try:
          while True:
            # Step 1: Wait for user input
            GPIO.output(LED_PIN, GPIO.LOW)
            lcd.lcd_clear()
            lcd.lcd_display_string("Place item", 1)
            lcd.lcd_display_string("in machine", 2)
            GPIO.wait_for_edge(IR_SENSOR_PIN, GPIO.RISING)
            
            #3-Second Delay after IR sensor Triggered
            lcd.lcd_clear()
            lcd.lcd_display_string("Item detected", 1)
            lcd.lcd_display_string("Processing...", 2)
            time.sleep(5)
            
            # Turn on LED for better image capture
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(5)
            
            # Buzzer Feedback
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(BUZZER_PIN,GPIO.LOW)
                        
            # Step 2: Capture and classify image
            image_path = "/home/pi/Pictures/captured_image.jpg"
            capture_image(image_path)
            
            lcd.lcd_clear()
            lcd.lcd_display_string("Image captured", 1)
            lcd.lcd_display_string("Classifying...", 2)
            time.sleep(5)
            
            # Classify the captured image
            image_url, classification_result, confidence_score = waste_classifier.capture_and_classification(image_path)
            confidende_score = float(confidence_score)
            
            
            # Turn off LED
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(5)
            
            # Step 3: Display classification result
            lcd.lcd_clear()
            lcd.lcd_display_string(f"{classification_result}", 1)
            lcd.lcd_display_string(f"Conf: {confidence_score:.2f}", 2)
            time.sleep(5)
            
            # Check if material is acceptable
            if classification_result not in ["Plastic", "Metal"]:
                lcd.lcd_clear()
                lcd.lcd_display_string("Invalid item", 1)
                lcd.lcd_display_string("Please remove", 2)
                time.sleep(5)
                continue
            
            lcd.lcd_clear()
            lcd.lcd_display_string("Valid item", 1)
            lcd.lcd_display_string("Processing...", 2)
            time.sleep(5)
            
            # Step 4: User decision
            user_choice = user_prompt()
            
            lcd.lcd_clear()
            lcd.lcd_display_string("Choice recorded", 1)
            lcd.lcd_display_string("Sorting item...", 2)
            time.sleep(5)
            
            # Step 5: Sort material
            if classification_result == "Plastic":
                servo_sort.sort_plastic()
                lcd.lcd_clear()
                lcd.lcd_display_string("Sorted to", 1)
                lcd.lcd_display_string("Plastic bin", 2)
                time.sleep(5)
            elif classification_result == "Metal":
                servo_sort.sort_metal()
                lcd.lcd_clear()
                lcd.lcd_display_string("Sorted to", 1)
                lcd.lcd_display_string("Metal bin", 2)
                time.sleep(5)
            time.sleep(2)
            
            ultrasonic_publisher.publish_sensor_data()
            material_count += 1
            
            lcd.lcd_clear()
            lcd.lcd_display_string(f"Total items: {material_count}", 1)
            lcd.lcd_display_string("Processing...", 2)
            time.sleep(5)
            
            # Step 6: Continue or cash out
            if user_choice == "stop":
                # Step 7: Dispense coins
                lcd.lcd_clear()
                lcd.lcd_display_string("Cashing out", 1)
                lcd.lcd_display_string(f"{material_count} coins", 2)
                time.sleep(5)
                
                lcd.lcd_clear()
                lcd.lcd_display_string("Dispensing", 1)
                lcd.lcd_display_string("Please wait...", 2)
                time.sleep(5)
                dispense_coins(material_count)
                
                # Publish ultrasonic sensor data
                lcd.lcd_clear()
                lcd.lcd_display_string("Publishing", 1)
                lcd.lcd_display_string("sensor data...", 2)
                time.sleep(5)
                
                # Reset and thank user
                material_count = 0
                lcd.lcd_clear()
                lcd.lcd_display_string("Thank you!", 1)
                lcd.lcd_display_string("Please come again", 2)
                time.sleep(5)
                continue  # Restart the loop
            
            lcd.lcd_clear()
            lcd.lcd_display_string("Ready for", 1)
            lcd.lcd_display_string("next item", 2)
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        GPIO.cleanup()
        mqtt_manager.disconnect()
        ultrasonic_publisher.cleanup()
        

if __name__ == "__main__":
    main()	
