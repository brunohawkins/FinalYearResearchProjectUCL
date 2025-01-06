import mujoco  # MuJoCo library
import mujoco.viewer as viewer  # Viewer for visualization

# Path to the Shadow Hand XML description file
xml_path = "/Users/brunohawkins/PycharmProjects/FinalYearResearchProjectUCL/Project_files/robotics_stuff/shadow_hand/right_hand.xml"

# Load the model from the XML file
model = mujoco.MjModel.from_xml_path(xml_path)

# Initialize the simulation data
data = mujoco.MjData(model)

# Launch the viewer and run the simulation
with viewer.launch_passive(model, data) as v:
    while v.is_running():
        mujoco.mj_step(model, data)