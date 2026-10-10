# LiDAR-Based Autonomous Obstacle Avoidance Using ROS 2 and Gazebo

## Overview

This project implements a differential-drive mobile robot in Gazebo Harmonic using ROS 2 Humble and Python.

A simulated GPU LiDAR provides distance measurements to a ROS 2 controller. The controller processes `LaserScan` data, detects nearby obstacles, and publishes velocity commands to navigate a simulated environment.

The robot is tested in a multi-obstacle course, where it navigates from START toward FINISH and stops when its programmed goal condition is reached.

## Features

- Custom differential-drive mobile robot
- GPU LiDAR simulation
- ROS 2–Gazebo integration using `ros_gz_bridge`
- LiDAR-based obstacle detection and avoidance
- Velocity control through `/cmd_vel`
- Robot odometry through `/odom`
- Multi-obstacle START-to-FINISH simulation
- Goal detection and automatic stopping

## Technologies Used

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

```text
my_lidar_demo/
├── launch/
│   ├── lidar_demo.launch.py
│   └── lidar_tf.launch.py
├── my_lidar_demo/
│   ├── __init__.py
│   └── obstacle_avoidance.py
├── resource/
├── rviz/
│   └── lidar.rviz
├── test/
├── worlds/
│   └── lidar_test.sdf
├── package.xml
├── setup.cfg
├── setup.py
├── .gitignore
└── README.md
```

## Prerequisites

Ensure that the following are installed and configured:

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Harmonic
- Required ROS–Gazebo bridge packages
- Colcon build tools

## How to Run

### 1. Build the Package

Open a terminal and run:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select my_lidar_demo
source ~/ros2_ws/install/setup.bash
```

### 2. Launch the Simulation

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch my_lidar_demo lidar_demo.launch.py
```

Keep this terminal running while the simulation is active.

### 3. Start the Obstacle Avoidance Controller

Open a second terminal and run:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run my_lidar_demo obstacle_avoidance
```

### 4. Monitor ROS 2 Topics

To check the available topics:

```bash
ros2 topic list
```

To inspect LiDAR measurements:

```bash
ros2 topic echo /lidar
```

To inspect robot odometry:

```bash
ros2 topic echo /odom
```

*Note: These commands assume the simulation and required ROS 2 nodes are running and publishing on the listed topics.*

## Results

The robot has been tested in a simulated multi-obstacle environment. It uses LiDAR distance measurements to detect nearby obstacles and adjust its motion through velocity commands. The controller also stops the robot when its programmed goal condition is reached.

The current implementation provides a foundation for further development of autonomous mobile robot navigation.

## Future Improvements

- Goal-directed path planning
- Improved obstacle avoidance and recovery behavior
- Quantitative evaluation of navigation performance
- Integration with the ROS 2 Navigation stack (Nav2)
- Testing under different obstacle configurations and simulation conditions

## Author

**Pushkar Suryavanshi**

## Repository

[GitHub – ROS 2 LiDAR Obstacle Avoidance](https://github.com/Pushkar1241/ros2-lidar-obstacle-avoidance)
