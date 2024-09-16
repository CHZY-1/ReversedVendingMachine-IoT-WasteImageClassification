import time
import picamera
import numpy as np
import tflite_runtime.interpreter as tflite
import cv2
import os
from datetime import datetime
import paho.mqtt.client as mqtt
import firebase_admin
from firebase_admin import credentials, storage, db

# Firebase setup
cred = credentials.Certificate("/home/pi/Desktop/waste_classification/pi-practical-firebase-adminsdk-68ehy-8a6c9c4b01.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'gs://pi-practical.appspot.com',
    'databaseURL': 'https://pi-practical-default-rtdb.firebaseio.com/'
})

bucket = storage.bucket()


# MQTT setup
broker_address = "localhost"
topic = "classification/results"
client = mqtt.Client()
client.connect(broker_address)


tflite_model = "/home/pi/Desktop/waste_classification/RaspberryPi-WasteImageClassification/model/model.tflite"
interpreter = tflite.Interpreter(model_path=tflite_model)
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Function to captures an image using the PiCamera and saves it to the specified path.
def capture_image():
    # Generate a unique file name using the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"/home/pi/Pictures/captured_image_{timestamp}.jpg"
    
    with picamera.PiCamera() as camera:
        # Set camera resolution
        camera.resolution = (1024, 768)
        
        # Allow the camera to warm up
        time.sleep(1)
        
        # Capture the image and save it to the specified path
        camera.capture(image_path)
    
    return image_path

# Function to preprocess the image
def preprocess_image(image_path):
    # Load image
    img = cv2.imread(image_path)
    
    # Resize image to match input size of the model (e.g., 224x224 for MobileNetV2)
    img_resized = cv2.resize(img, (224, 224))
    
    # Convert image to float32 and normalize to range [-1, 1] (MobileNetV2 preprocessing)
    img_normalized = img_resized.astype(np.float32)
    img_normalized = (img_normalized / 127.5) - 1.0
    
    # Expand dimensions to match model's input shape (1, 224, 224, 3)
    img_batch = np.expand_dims(img_normalized, axis=0)
    
    return img_batch

# Function to run inference
def run_inference(image_path):
    # Preprocess the image
    input_data = preprocess_image(image_path)
    
    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)
    
    # Run the inference
    interpreter.invoke()
    
    # Get the output (class probabilities)
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Find the class with the highest probability
    predicted_class = np.argmax(output_data)

    # Get the confidence score
    confidence_score = np.max(output_data)
    
    return predicted_class, confidence_score, output_data

# Upload image to Firebase Storage and return the URL
def upload_image_to_firebase(image_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"image_{timestamp}.jpg"
    blob = bucket.blob(f"folder/{file_name}")
    blob.upload_from_filename(image_path)
    blob.make_public()
    return blob.public_url

# Store classification result in Firebase Realtime Database
def store_to_firebase_db(image_url, classification_result, confidence_score):
    ref = db.reference('classification_results')
    ref.push({
        'imageUrl': image_url,
        'classificationResult': classification_result,
        'confidenceScore': confidence_score,
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
    })

# Publish result to MQTT topic
def publish_to_mqtt(image_url, classification_result, confidence_score):
    data = {
        "imageUrl": image_url,
        "classificationResult": classification_result,
        "confidenceScore": confidence_score
    }
    client.publish(topic, str(data))

# Map the predicted class to labels
def map_class_to_label(predicted_class):
    if predicted_class == 3:
        return "Plastic"
    elif predicted_class == 6:
        return "Metal"
    else:
        return "Others"

if __name__ == "__main__":
    image_path = "/home/pi/Pictures/captured_image.jpg"
    
    # Capture an image and get the image path with timestamp
    # image_path = capture_image()
    
    # Run inference on the captured image
    predicted_class, confidence_score, probabilities = run_inference(image_path)
    
    # Map the predicted class to a label
    label = map_class_to_label(predicted_class)
    
    # Print the classification result and confidence level
    print(f"classification_result: {label}")
    print(f"confidence_level: {confidence_score}")


if __name__ == "__main__":
    # Capture an image
    image_path = capture_image()
    
    # Run inference on the captured image
    predicted_class, confidence_score, _ = run_inference(image_path)
    
    # Map the predicted class to a label
    classification_result = map_class_to_label(predicted_class)
    
    # Upload the image to Firebase Storage and get the URL
    image_url = upload_image_to_firebase(image_path)
    
    # Store classification result and image URL in Firebase Realtime Database
    # store_to_firebase_db(image_url, classification_result, confidence_score)
    
    # Publish the result to an MQTT topic
    publish_to_mqtt(image_url, classification_result, confidence_score)
    
    print(f"Image URL: {image_url}")
    print(f"Classification Result: {classification_result}")
    print(f"Confidence Score: {confidence_score}")