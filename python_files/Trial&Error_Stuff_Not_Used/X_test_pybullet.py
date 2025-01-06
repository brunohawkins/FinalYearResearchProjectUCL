import pybullet as p
import time

# Connect to PyBullet in GUI mode
p.connect(p.GUI)

# Create a simple plane (no need for URDF)
plane_id = p.createCollisionShape(p.GEOM_PLANE)
plane_visual = p.createVisualShape(p.GEOM_PLANE)
plane = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=plane_id, baseVisualShapeIndex=plane_visual)

# Create a simple cube (no URDF)
cube_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.5])  # Cube dimensions (x, y, z)
cube_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.5], rgbaColor=[0, 1, 0, 1])  # Green color
cube = p.createMultiBody(baseMass=1, basePosition=[0, 0, 1], baseCollisionShapeIndex=cube_id, baseVisualShapeIndex=cube_visual)

# Run the simulation for a bit
for _ in range(10000):
    p.stepSimulation()  # Step the simulation forward
    time.sleep(1./240.)  # Sleep to match the simulation time step (240 Hz)

# Disconnect from the PyBullet environment
p.disconnect()
