# Drone Automation Starter Repo (Production-ready scaffold)

This repository is a production-ready starter pack for autonomous drone development.
It contains runnable DroneKit missions, vision-based tracking, AI obstacle avoidance,
a simple UDP swarm demo, ROS2 nodes for integration, PX4/ArduPilot SITL configs,
Jetson deployment notes, systemd services, and a permissive MIT license.

## Structure
- mission/            - DroneKit mission scripts and helpers
- vision/             - OpenCV tracking and camera utilities
- avoidance/          - YOLO + RealSense avoidance pipeline
- swarm/              - Leader / follower UDP demo
- ros2_nodes/         - ROS2 nodes (talker/bridge for MAVROS)
- sim/                - SITL and PX4 simulation helpers
- jetson/             - Jetson optimization & deployment scripts
- systemd/            - example systemd unit files
- configs/            - example flight controller parameter files
- LICENSE
- README.md

## Quickstart (simulation)
1. Create venv and install deps:
   ```bash
   python3 -m venv venv && source venv/bin/activate
   pip install --upgrade pip
   pip install dronekit pymavlink opencv-python numpy ultralytics pyrealsense2 pyproj
   # Optional for ROS2 integration: install ROS2 and mavros on your system
   ```

2. Start ArduPilot SITL (example):
   ```bash
   sim_vehicle.py -v ArduCopter -f quad --console --map
   ```

3. Run mission:
   ```bash
   python mission/mission.py --connect 127.0.0.1:14550
   ```

4. Test vision:
   ```bash
   python vision/object_tracking.py --camera 0
   ```

## Safety
- Bench test without props.
- Use a safety net and a tether for first flights.
- Follow local regulations.

