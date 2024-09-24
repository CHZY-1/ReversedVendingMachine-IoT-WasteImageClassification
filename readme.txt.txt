Project : Reverse Recycle Bin System

This repository contains the source code, configurations, and other relevant files for the Reverse Recycle Bin System, which classifies and sorts waste using MobileNetV2 for image classification, integrated with Raspberry Pi hardware components for real-time waste management.

Main Folder and File Descriptions

Folders

-fineTuning: Holds scripts and configuration files related to the fine-tuning of the MobileNetV2 model.

-mobilenet-v2-keras-weights: Contains pre-trained MobileNetV2 weights used in the waste classification model.

-model: Stores trained models (different version of model) and Jupyter notebook for fine tuning the model.

-node_red: Node-RED exported flows

-trainingData: Contains images used for training the classification model, including datasets of plastic and metal items.


Files

-I2C_LCD_driver.py: Python script for interfacing with the I2C LCD display, used for displaying bin levels and classification results.

-mqtt_remote_subscribe_test.py: Script to test the MQTT subscription functionality for receiving data from sensors and classification results.

-MQTTManager.py: Manages MQTT connections, subscriptions, and publishing of data for the system.

-RVM.py: Main script managing the Reverse Vending Machine (RVM) functionality, integrating various sensors and actuators. Run This script to start the system.

-servo_motor.py: Controls the servo motor actions, such as opening and closing the bin lid.

-UltrasonicSensorPublish.py: Control and Publishes ultrasonic sensor data to monitor bin levels in real-time.

-WasteClassifier.py: Contains the logic for loading the fine-tuned MobileNetV2 model and running waste classification tasks.
