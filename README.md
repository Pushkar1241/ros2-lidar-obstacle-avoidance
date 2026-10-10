# LiDAR-Based Autonomous Obstacle Avoidance Using ROS 2 and Gazebo

## Overview

This project implements a differential-drive mobile robot in Gazebo Harmonic using ROS 2 Humble and Python.

A simulated GPU LiDAR provides distance measurements to a ROS 2 controller. The controller processes LaserScan data, detects nearby obstacles, and publishes velocity commands to navigate the simulated environment.

## Features

- Custom differential-drive mobile robot
- GPU LiDAR simulation
- ROS 2 and Gazebo integration using `ros_gz_bridge`
- LiDAR-based obstacle avoidance
- Velocity control using `/cmd_vel`
- Robot odometry using `/odom`
- Multi-obstacle START-to-FINISH simulation
- Goal detection and automatic stopping

## Technologies

- ROS 2 Humble
- Gazebo Harmonic
- Python 3
- RViz2
- `ros_gz_bridge`
- Ubuntu 22.04

## ROS 2 Topics

| Topic | Purpose |
|---|---|
| `/lidar` | LiDAR distance measurements |
| `/cmd_vel` | Robot velocity commands |
| `/odom` | Robot position and motion information |
| `/tf` | Coordinate transforms |

## Project Structure

- `my_lidar_demo/obstacle_avoidance.py` — obstacle avoidance controller
- `worlds/lidar_test.sdf` — robot and obstacle-course simulation
- `launch/lidar_demo.launch.py` — launches the simulation
- `launch/lidar_tf.launch.py` — LiDAR transform launch configuration
- `rviz/lidar.rviz` — RViz visualization configuration

## How to Run

Build the package:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select my_lidar_demo
source ~/ros2_ws/install/setup.bash
```

Start the simulation:

```bash
ros2 launch my_lidar_demo lidar_demo.launch.py
```

In a second terminal, start the controller:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run my_lidar_demo obstacle_avoidance
```

## Results

The robot has been tested in a simulated multi-obstacle course. It uses LiDAR measurements to avoid obstacles and stops when its programmed goal condition is reached.

## Future Improvements

- Goal-directed path planning
- Improved obstacle avoidance
- Quantitative navigation performance evaluation
- Integration with ROS 2 navigation tools

## Author

Pushkar Suryavanshi
