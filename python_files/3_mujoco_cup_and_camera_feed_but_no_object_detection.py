#NOT WORKING. NEED TO CONTINUE ON A WINDOWS PC OR SOMETHING THAT SUPPORTS OPENGL

import mujoco
import numpy as np

# Path to your MuJoCo XML file
xml_path = "/Users/brunohawkins/PycharmProjects/FinalYearResearchProjectUCL/Project_files/robotics_stuff/Testing_mujoco_environment/mujoco_test_cup_and_camera.xml"

# Load the MuJoCo model and data
model = mujoco.MjModel.from_xml_path(xml_path)
data = mujoco.MjData(model)

# Create an offscreen renderer
renderer = mujoco.MjrContext(model, mujoco.mjtFontScale.mjFONTSCALE_150)
viewport = mujoco.MjrRect(0, 0, 640, 480)

def get_camera_frame(model, data, camera_name="cup_camera"):
    cam_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, camera_name)
    if cam_id == -1:
        raise ValueError(f"Camera '{camera_name}' not found in the MuJoCo model.")

    # Create an array to hold the RGB frame
    rgb_array = np.zeros((viewport.height, viewport.width, 3), dtype=np.uint8)

    # Render the camera view to the frame buffer
    mujoco.mjv_updateScene(model, data, None, None, mujoco.mjvScene(), None, None, cam_id)
    mujoco.mjr_render(viewport, mujoco.mjvScene(), renderer)
    mujoco.mjr_readPixels(rgb_array, None, viewport)

    return rgb_array

try:
    for _ in range(100):  # Capture 100 frames
        mujoco.mj_step(model, data)
        frame = get_camera_frame(model, data)
        print("Captured a frame successfully!")

except Exception as e:
    print(f"Error occurred: {e}")
