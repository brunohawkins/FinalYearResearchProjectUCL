import mujoco
import mujoco.viewer as viewer

model_path = "/Users/brunohawkins/PycharmProjects/FinalYearResearchProjectUCL/Project_files/robotics_stuff/shadow_hand/scene_right.xml"
model = mujoco.MjModel.from_xml_path(model_path)
data = mujoco.MjData(model)

with viewer.launch(model, data) as v:
    while v.is_running():
        mujoco.mj_step(model, data)
