from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    lidar_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', '0',
            '--y', '0',
            '--z', '0.23',
            '--roll', '0',
            '--pitch', '0',
            '--yaw', '0',
            '--frame-id', 'lidar_robot/base_link',
            '--child-frame-id', 'lidar_robot/base_link/gpu_lidar'
        ],
        output='screen'
    )

    return LaunchDescription([
        lidar_tf
    ])
