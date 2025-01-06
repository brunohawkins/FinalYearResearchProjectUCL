import torch
import cv2
from PIL import Image
import numpy as np
from ultralytics import YOLO

# Load the YOLOv11 model
model_path = '/Users/brunohawkins/PycharmProjects/FinalYearResearchProjectUCL/Project_files/object_detection_model/best.pt'
model = YOLO("/Users/brunohawkins/PycharmProjects/FinalYearResearchProjectUCL/Project_files/object_detection_model/yolo11n.pt")

# Initialize video capture for MacBook's built-in camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened correctly
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Define the class IDs for "mug" and "cup" (ensure these match your model's classes)
mug_class_id = 77  # You may need to adjust this if the model's class ID is different
cup_class_id = 41  # You may need to adjust this if the model's class ID is different

# Define a function to process each frame
def detect_objects(frame):
    # Convert the frame to RGB (OpenCV uses BGR by default)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Convert to PIL Image for YOLO
    pil_img = Image.fromarray(rgb_frame)
    # Run the model
    results = model(pil_img)

    # Now, results is a list of detected objects
    if len(results) > 0:
        result = results[0]  # Assuming we only have one result object
        if result is not None and result.boxes is not None:
            # Accessing the bounding boxes
            boxes = result.boxes  # A tensor of bounding boxes
            for box in boxes:
                # Extract the coordinates and class info
                x1, y1, x2, y2 = box.xyxy[0].tolist()  # Extract box as [x1, y1, x2, y2]
                conf = box.conf[0].item()  # Confidence score
                cls = int(box.cls[0].item())  # Class index

                # Only draw boxes for 'cup' (41) and 'mug' (77)
                if cls == cup_class_id or cls == mug_class_id:
                    label = f"{model.names[cls]} {conf:.2f}"

                    # Draw the bounding box around the object
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    # Draw the label above the bounding box
                    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

print("Press 'q' to quit.")

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Detect objects in the frame
    result_frame = detect_objects(frame)

    # Display the frame with detections
    cv2.imshow('YOLO Real-Time Detection - Mugs and Cups', result_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
