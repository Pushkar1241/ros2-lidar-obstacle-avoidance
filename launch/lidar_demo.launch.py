import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    package_share = get_package_share_directory(
        'my_lidar_demo'
    )

    world_file = os.path.join(
        package_share,
        'worlds',
        'lidar_test.sdf'
    )

    rviz_config = os.path.join(
        package_share,
        'rviz',
        'lidar.rviz'
    )


    # ==========================================
    # GAZEBO
    # ==========================================

    gazebo = ExecuteProcess(
        cmd=[
            'gz',
            'sim',
            '-r',
            world_file
        ],
        output='screen'
    )


    # ==========================================
    # ROS <-> GAZEBO BRIDGE
    # ==========================================

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',

        arguments=[
            '/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
        ],

        output='screen'
    )


    # ==========================================
    # LiDAR TF
    # ==========================================

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

            '--frame-id',
            'lidar_robot/base_link',

            '--child-frame-id',
            'lidar_robot/base_link/gpu_lidar',
        ],

        output='screen'
    )


    # ==========================================
    # RVIZ
    # ==========================================

    rviz = Node(
        package='rviz2',
        executable='rviz2',

        arguments=[
            '-d',
            rviz_config
        ],

        output='screen'
    )


    return LaunchDescription([
        gazebo,
        bridge,
        lidar_tf,
        rviz
    ])
