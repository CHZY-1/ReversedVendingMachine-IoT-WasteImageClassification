import paho.mqtt.client as mqtt

# MQTT settings
pi_hostname = "raspberry-pi-5"
topic = "classification/results"

# Define the callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
    else:
        print(f"Failed to connect, return code {rc}")

# Define the callback when a message is received on the subscribed topic
def on_message(client, userdata, message):
    print(f"Received message on {message.topic}: {message.payload.decode()}")

# Function to connect to MQTT and start the loop
def start_mqtt_client():
    # Create an MQTT client instance
    client = mqtt.Client()

    # Attach the callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the Raspberry Pi MQTT broker using its hostname or IP address
    try:
        print(f"Connecting to MQTT broker at {pi_hostname}...")
        client.connect(pi_hostname)
    except Exception as e:
        print(f"Failed to connect to {pi_hostname}: {e}")
        return

    # Start the loop to process incoming and outgoing MQTT messages
    client.loop_forever()

if __name__ == "__main__":
    start_mqtt_client()
