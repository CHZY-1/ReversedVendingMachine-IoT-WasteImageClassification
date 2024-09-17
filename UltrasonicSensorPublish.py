import RPi.GPIO as GPIO
import time
import json
import paho.mqtt.client as mqtt

class UltrasonicSensorPublisher:
    def __init__(self, sensors, broker_address="localhost", topic="sensors/ultrasonic"):
        """
        Initialize the UltrasonicSensorPublisher class.

        :param sensors: List of dictionaries, each containing trigger and echo pin numbers for each ultrasonic sensor.
        example : 
        # List of sensors with trigger and echo pins
        sensors = [
            {"trigger": 23, "echo": 24},  # Ultrasonic Sensor 1
            {"trigger": 27, "echo": 22},  # Ultrasonic Sensor 2
            # More
        ]

        :param broker_address: MQTT broker address (default: "localhost").
        :param topic: MQTT topic to publish the sensor data (default: "sensors/ultrasonic").
        """

        # MQTT setup
        self.client = mqtt.Client()
        self.client.connect(broker_address)
        self.topic = topic

        # GPIO setup

        # List of sensor dictionaries with trigger/echo pin info
        self.sensors = sensors

        # Use BCM GPIO numbering - Use GPIO number to configure trig and echo
        GPIO.setmode(GPIO.BCM)

        for sensor in self.sensors:
            GPIO.setup(sensor["trigger"], GPIO.OUT)
            GPIO.setup(sensor["echo"], GPIO.IN)
            GPIO.output(sensor["trigger"], GPIO.LOW)

        time.sleep(2)  # Allow sensors to settle

    # Function to measure distance for a given trigger and echo pin
    def measure_distance(self, trigger_pin, echo_pin):
        # Send a 10us pulse to trigger the ultrasonic sensor
        GPIO.output(trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)  # 10 microseconds
        GPIO.output(trigger_pin, GPIO.LOW)

        # Measure the duration of the echo pulse
        while GPIO.input(echo_pin) == 0:
            pulse_start = time.time()

        while GPIO.input(echo_pin) == 1:
            pulse_end = time.time()

        # Calculate distance based on the duration of the pulse
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Speed of sound in cm/s (34300 cm/s / 2)
        distance = round(distance, 2)  # Round the distance to 2 decimal places

        return distance

    # Publish sensor data to MQTT
    def publish_sensor_data(self):
        # Dictionary to store sensor data
        sensor_data = {}

        # Measure distance from all sensors
        for index, sensor in enumerate(self.sensors):
            distance = self.measure_distance(sensor["trigger"], sensor["echo"])
            sensor_data[f"ultrasonic_sensor_{index+1}"] = distance

        # Publish the data as a serialized JSON string
        json_data = json.dumps(sensor_data)
        self.client.publish(self.topic, json_data)
        print(f"Published: {json_data}")

    # Clean up GPIO pins
    def cleanup(self):
        GPIO.cleanup()



# Import this
def publish_ultrasonic_sensor_data(sensors : list[dict]):
    """ Param : sensors -> example
    sensors = [
            {"trigger": 23, "echo": 24},  # Ultrasonic Sensor 1
            {"trigger": 17, "echo": 22},  # Ultrasonic Sensor 2
        ]
    """

    sensor_publisher = UltrasonicSensorPublisher(sensors=sensors, broker_address="localhost", topic="sensors/ultrasonic")

    sensor_publisher.publish_sensor_data()

    sensor_publisher.cleanup()



if __name__ == "__main__":
    try:
        # List of sensors with trigger and echo pins
        sensors = [
            {"trigger": 23, "echo": 24},  # Ultrasonic Sensor 1
        ]

        # Initialize the ultrasonic sensor class
        sensor_publisher = UltrasonicSensorPublisher(sensors=sensors, broker_address="localhost", topic="sensors/ultrasonic")

        # Continuously publish sensor data
        while True:
            sensor_publisher.publish_sensor_data()
            time.sleep(1)  # Wait 1 second before the next reading

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        sensor_publisher.cleanup()
