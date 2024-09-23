import time
import numpy as np
import tflite_runtime.interpreter as tflite
import cv2
import os
import json
from datetime import datetime
import paho.mqtt.client as mqtt
import firebase_admin
from firebase_admin import credentials, storage, db

class WasteClassifier:
    firebase_initialized = False
    bucket = None

    def __init__(self, mqtt_manager, model_path, topic="classification/results"):
        if not WasteClassifier.firebase_initialized:
            self.initialize_firebase()

        # Initialize MQTT
        self.mqtt_manager = mqtt_manager
        self.topic = topic
        
        # Load the TFLite model and allocate tensors
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # Get input and output tensors
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    @classmethod
    def initialize_firebase(cls):
        """Initialize Firebase only once at the class level."""

        cred = credentials.Certificate("/home/pi/Desktop/waste_classification/pi-practical-firebase-adminsdk-68ehy-f8d78e7883.json")
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'pi-practical.appspot.com',
            'databaseURL': 'https://pi-practical-default-rtdb.firebaseio.com/'
        })
        cls.bucket = storage.bucket()
        cls.firebase_initialized = True

    # Preprocess the image
    def preprocess_image(self, image_path):
        img = cv2.imread(image_path)
        img_resized = cv2.resize(img, (128, 128))
        img_normalized = img_resized.astype(np.float32)
        img_normalized = (img_normalized / 127.5) - 1.0
        img_batch = np.expand_dims(img_normalized, axis=0)
        return img_batch
    
    def run_inference(self, image_path):
        """Run inference on the image using the TFLite model."""
        input_data = self.preprocess_image(image_path)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        predicted_class = np.argmax(output_data)
        confidence_score = np.max(output_data)
        return predicted_class, confidence_score
    
    # Upload image to Firebase Storage and return the URL
    def upload_image_to_firebase(self, image_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"image_{timestamp}.jpg"
        blob = WasteClassifier.bucket.blob(f"folder/{file_name}")
        blob.upload_from_filename(image_path)
        blob.make_public()
        return blob.public_url
    
    # Publish result to MQTT topic
    def publish_to_mqtt(self, image_url, classification_result, confidence_score):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {
            "imageUrl": image_url,
            "classificationResult": classification_result,
            "confidenceScore": float(confidence_score),
            "timestamp": timestamp
        }
        json_data = json.dumps(data)
        self.mqtt_manager.publish(self.topic, json_data)
    
    # Map the predicted class to labels
    def map_class_to_label(self, predicted_class):
        if predicted_class == 2:
            return "Plastic"
        elif predicted_class == 4:
            return "Metal"
        else:
            return "Others"	
        

    def capture_and_classification(self, image_path):
        """
        Perform classification on the captured image and handle related operations.
        
        :param image_path: Path to the captured image file
        :return: Tuple containing (image_url, classification_result, confidence_score)
        """
        try:
            # Run inference on the captured image
            predicted_class, confidence_score = self.run_inference(image_path)
            
            # Map the predicted class to a label
            classification_result = self.map_class_to_label(predicted_class)
            
            # Upload the image to Firebase Storage and get the URL
            image_url = self.upload_image_to_firebase(image_path)
            
            # Publish the result to an MQTT topic
            self.publish_to_mqtt(image_url, classification_result, confidence_score)
            
            print(f"Image URL: {image_url}")
            print(f"Classification Result: {classification_result}")
            print(f"Confidence Score: {confidence_score}")
            
            return image_url, classification_result, confidence_score

        except Exception as e:
            print(f"Error in capture_and_classification: {str(e)}")
            # Return default values or handle the error as appropriate for your application
            return None, "Error", 0.0