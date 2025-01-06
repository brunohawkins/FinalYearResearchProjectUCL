import mujoco
from mujoco.viewer import launch_passive

# Path to your MuJoCo XML file
xml_path = "/Users/brunohawkins/PycharmProjects/FinalYearResearchProjectUCL/Project_files/robotics_stuff/Testing_mujoco_environment/mujoco_test_cup.xml"

# Load the model and data
model = mujoco.MjModel.from_xml_path(xml_path)
data = mujoco.MjData(model)

# Keep the viewer open
print("Launching the MuJoCo viewer. Close the viewer manually to exit.")
launch_passive(model, data)

# Keep the script running to prevent the viewer from closing
try:
    while True:
        pass  # Infinite loop to keep the viewer open
except KeyboardInterrupt:
    print("Viewer closed.")
