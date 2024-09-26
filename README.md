# Smart Recycling Bin with Image Classification and Raspberry Pi Integration

This project features a smart reverse recycling bin that uses a camera and image classification (MobileNetV2) to automatically sort waste into plastic or metal. The image classifier is fine-tuned with real images from the prototype.


The system runs on two Raspberry Pi devices:

- Raspberry Pi 1 controls the bin’s sensors, handles waste classification, and sends data through MQTT.
- Raspberry Pi 2 subscribes to MQTT topics, uploads data to Firebase, and displays it on a real-time dashboard built with Node-Red.


## System Design

![overview](diagram/block-diagram.png)

![GPIO](diagram/RVM-GPIO.png)

![MQTT](diagram/MQTT.png)

Raspberry Pi 1
![flowchart-pi1](diagram/flow-chart-localhost-publisher.png)

Raspberry Pi 2
![flowchart-pi1](diagram/flow-chart-remote-subscriber.png)

## Prototype

![prototype](diagram/prototype-1.png)

![prototype](diagram/prototype-2-camera.png)

![prototype](diagram/prototype-2-coin-dispenser.png)

![prototype](diagram/prototype-2-hardware-gpio.png)

![prototype](diagram/prototype-2-led-buzzer-IR.png)

![prototype](diagram/prototype-2-sorting-platform.png)

## Visualization

![Node-Red](diagram/node-red-firebase-dashboard.png)

![dashboard](diagram/RVM-dashboard.png)