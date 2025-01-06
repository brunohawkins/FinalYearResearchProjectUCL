import pybullet as p
import pybullet_data
import time

# Connect to PyBullet (GUI mode)
p.connect(p.GUI)

# Set search path for URDFs
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load ground plane and robot
p.loadURDF("/Users/brunohawkins/PycharmProjects/FinalYearResearchProjectUCL/Project_files/pybullet_ground_plane.urdf")
robot = p.loadURDF("/Users/brunohawkins/PycharmProjects/FinalYearResearchProjectUCL/Project_files/pybullet_test_robot.urdf", basePosition=[0, 0, 0])

# Fix the base link to the world
base_constraint = p.createConstraint(
    parentBodyUniqueId=robot,
    parentLinkIndex=-1,  # Base link
    childBodyUniqueId=-1,
    childLinkIndex=-1,
    jointType=p.JOINT_FIXED,
    jointAxis=[0, 0, 0],
    parentFramePosition=[0, 0, 0],
    childFramePosition=[0, 0, 0]
)

# Create a debug slider for the hinge joint
slider = p.addUserDebugParameter("Hinge Position", -1.57, 1.57, 0)

# Run simulation and use the slider to control the joint
p.setGravity(0, 0, -9.8)
for i in range(10000):
    # Read slider value
    target_position = p.readUserDebugParameter(slider)

    # Apply joint position control
    p.setJointMotorControl2(
        bodyIndex=robot,
        jointIndex=0,  # Index of the hinge joint
        controlMode=p.POSITION_CONTROL,
        targetPosition=target_position,
        force=10.0
    )
    p.stepSimulation()
    time.sleep(1/240)  # Slow down the simulation for viewing
