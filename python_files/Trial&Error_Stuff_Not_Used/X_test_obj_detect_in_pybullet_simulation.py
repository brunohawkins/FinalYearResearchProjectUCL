import pybullet as p
import numpy as np
import time
from PIL import Image
import cv2
from ultralytics import YOLO

# Connect to PyBullet
p.connect(p.GUI)

# Camera settings
camera_distance = 10
camera_yaw = 50
camera_pitch = -20
camera_target_position = [0, 0, 0]

# Create collision and visual shapes for the mug
obj_file_path = '/Users/brunohawkins/Library/CloudStorage/OneDrive-UniversityCollegeLondon/UCL stuff/Medical Sciences & Engineering BSc (Hons)/Year 3/SURG0161/Resources for the project/3D models/cup obj singular.obj'
scaling_factor = 0.05

collision_shape_id = p.createCollisionShape(
    p.GEOM_MESH,
    fileName=obj_file_path,
    meshScale=[scaling_factor, scaling_factor, scaling_factor]
)
visual_shape_id = p.createVisualShape(
    p.GEOM_MESH,
    fileName=obj_file_path,
    meshScale=[scaling_factor, scaling_factor, scaling_factor]
)

# Create the mug as a fixed object
mug_id = p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=collision_shape_id,
    baseVisualShapeIndex=visual_shape_id,
    basePosition=[0, 0, 0.1]
)

# Create the view and projection matrices for the camera
view_matrix = p.computeViewMatrixFromYawPitchRoll(
    cameraTargetPosition=camera_target_position,
    distance=camera_distance,
    yaw=camera_yaw,
    pitch=camera_pitch,
    roll=0,
    upAxisIndex=2
)

projection_matrix = p.computeProjectionMatrixFOV(
    fov=60,
    aspect=1.0,
    nearVal=0.1,
    farVal=100.0
)

# Load YOLOv11 model with pretrained weights
weights_path = "/Users/brunohawkins/PycharmProjects/FinalYearResearchProjectUCL/Project_files/object_detection_model/best.pt"
model = YOLO(weights_path)

# Function to capture the image
def capture_image():
    # Capture the image using the view and projection matrices
    width, height, rgbImg, _, _ = p.getCameraImage(
        width=640,
        height=480,
        viewMatrix=view_matrix,
        projectionMatrix=projection_matrix,
        renderer=p.ER_BULLET_HARDWARE_OPENGL
    )

    # Convert to a NumPy array and ensure correct dtype
    image = np.array(rgbImg, dtype=np.uint8)
    image = image[:, :, :3]  # Remove the alpha channel if it exists
    return cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)  # Ensure RGB format

# Function to run the detection model
def detect_objects(image):
    results = model(image)  # Perform inference
    detections = []

    # Iterate through results and extract detection details
    for result in results:  # 'results' is a list of Results objects
        for box in result.boxes:  # Access each detected bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            confidence = box.conf.item()  # Confidence score
            class_id = int(box.cls.item())  # Class ID
            detections.append((x1, y1, x2, y2, confidence, class_id))

    return detections


# Define class names (replace with your model's class names if needed)
class_names = ["Cup", "Mug", "Glass"]  # Example


def draw_boxes(image, detections):
    print(f"Image type: {type(image)}, dtype: {image.dtype}, shape: {image.shape}")
    for detection in detections:
        x1, y1, x2, y2, confidence, class_id = detection
        label = f"Class {class_id} {confidence:.2f}"

        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Add text label
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return image


# Keep simulation running and detect objects in real-time
while True:
    # Capture image from PyBullet
    image = capture_image()

    # Run detection model
    detections = detect_objects(image)

    # Draw bounding boxes (optional, for visualization)
    image_with_boxes = draw_boxes(image, detections)

    # Display the image with detected objects
    cv2.imshow("Detected Objects", image_with_boxes)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Step the simulation
    p.stepSimulation()
    time.sleep(1./240.)

# Disconnect from PyBullet and cleanup
p.disconnect()
cv2.destroyAllWindows()
