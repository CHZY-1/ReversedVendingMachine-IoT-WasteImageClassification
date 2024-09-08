import numpy as np
import tflite_runtime.interpreter as tflite
import cv2

# Load the TFLite model and allocate tensors
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

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
    
    return predicted_class, output_data

# Map the predicted class to labels
def map_class_to_label(predicted_class):
    if predicted_class == 3:
        return "Plastic"
    else:
        return "Non-Plastic"

# Main script to test the inference
if __name__ == "__main__":
    # Replace this with the path to your test image
    image_path = "plastic_bottle.jpg"
    
    # Run inference on the image
    predicted_class, probabilities = run_inference(image_path)
    
    # Map the predicted class to a label
    label = map_class_to_label(predicted_class)
    
    # Print the result
    print("Predicted Class: " + label)
    print("Probabilities: " + probabilities)