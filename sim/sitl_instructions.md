# SITL / Simulator Instructions

## ArduPilot SITL (simple)
1. Install ArduPilot Dev environment (see ardupilot.org)
2. Launch SITL:
   sim_vehicle.py -v ArduCopter -f quad --console --map
3. Connect DroneKit scripts to 127.0.0.1:14550

## PX4 SITL + Gazebo
Follow PX4 dev guide: `make px4_sitl_default gazebo`
Connect to 127.0.0.1:14540 or as reported by PX4.
