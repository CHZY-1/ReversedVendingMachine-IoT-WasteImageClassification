import paho.mqtt.client as mqtt
import json

class MQTTManager:
    def __init__(self, broker_address="localhost", port=1883):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker_address = broker_address
        self.port = port
        self.subscriptions = {}

    def connect(self):
        self.client.connect(self.broker_address, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"MQTT Connected with result code {rc}")
        for topic in self.subscriptions:
            self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        if msg.topic in self.subscriptions:
            self.subscriptions[msg.topic](msg.payload)

    def publish(self, topic, message):
        self.client.publish(topic, json.dumps(message))

    # def subscribe(self, topic, callback):
    #   self.subscriptions[topic] = callback
    #   if self.client.is_connected():
    #       self.client.subscribe(topic)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

if __name__ =="__main__":
    mqtt_manager = MQTTManager(broker_address="RVMPi.local")
    mqtt_manager.connect()

    # In UltrasonicSensorPublisher
    def publish_ultrasonic_data(data):
        mqtt_manager.publish("sensors/ultrasonic", data)

    # In WasteClassifier
    def publish_classification_data(data):
        mqtt_manager.publish("classification/results", data)

    # Subscription example
    def handle_ultrasonic_data(payload):
        data = json.loads(payload)
        print(f"Received ultrasonic data: {data}")

    def handle_classification_data(payload):
        data = json.loads(payload)
        print(f"Received classification data: {data}")

    mqtt_manager.subscribe("sensors/ultrasonic", handle_ultrasonic_data)
    mqtt_manager.subscribe("classification/results", handle_classification_data)
