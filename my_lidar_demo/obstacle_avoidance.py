#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class ObstacleAvoidance(Node):

    def __init__(self):

        super().__init__('obstacle_avoidance')

        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.lidar_subscriber = self.create_subscription(
            LaserScan,
            '/lidar',
            self.lidar_callback,
            10
        )

        self.odom_subscriber = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.forward_speed = 0.30
        self.turn_speed = 0.60

        self.obstacle_distance = 1.0
        self.clear_distance = 1.5

        self.finish_x = 16.5

        self.state = "MOVING"

        self.latest_scan = None

        self.robot_x = 0.0
        self.robot_y = 0.0

        self.last_reported_state = ""

        self.timer = self.create_timer(
            0.1,
            self.control_robot
        )

        self.get_logger().info(
            'Autonomous obstacle avoidance started.'
        )

        self.get_logger().info(
            f'Finish position: x >= {self.finish_x:.2f} m'
        )


    def lidar_callback(self, msg):

        self.latest_scan = msg


    def odom_callback(self, msg):

        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y


    def get_sector_min_distance(
        self,
        start_angle_deg,
        end_angle_deg
    ):

        if self.latest_scan is None:

            return float('inf')

        scan = self.latest_scan

        start_angle = math.radians(
            start_angle_deg
        )

        end_angle = math.radians(
            end_angle_deg
        )

        valid_distances = []

        for i, distance in enumerate(
            scan.ranges
        ):

            angle = (
                scan.angle_min
                + i * scan.angle_increment
            )

            if (
                start_angle
                <= angle
                <= end_angle
            ):

                if math.isfinite(distance):

                    if (
                        scan.range_min
                        <= distance
                        <= scan.range_max
                    ):

                        valid_distances.append(
                            distance
                        )

        if not valid_distances:

            return float('inf')

        return min(valid_distances)


    def control_robot(self):

        if self.latest_scan is None:

            return


        if self.state == "FINISHED":

            self.stop_robot()

            return


        if self.robot_x >= self.finish_x:

            self.state = "FINISHED"

            self.stop_robot()

            self.get_logger().info(
                '================================'
            )

            self.get_logger().info(
                '        GOAL REACHED!'
            )

            self.get_logger().info(
                f'Final position: '
                f'X = {self.robot_x:.2f} m, '
                f'Y = {self.robot_y:.2f} m'
            )

            self.get_logger().info(
                'Robot stopped at the finish.'
            )

            self.get_logger().info(
                '================================'
            )

            return


        front_distance = (
            self.get_sector_min_distance(
                -15,
                15
            )
        )

        left_distance = (
            self.get_sector_min_distance(
                30,
                120
            )
        )

        right_distance = (
            self.get_sector_min_distance(
                -120,
                -30
            )
        )


        cmd = Twist()


        if self.state == "MOVING":

            if (
                front_distance
                < self.obstacle_distance
            ):

                cmd.linear.x = 0.0

                if left_distance > right_distance:

                    self.state = "TURNING_LEFT"

                    cmd.angular.z = (
                        self.turn_speed
                    )

                else:

                    self.state = "TURNING_RIGHT"

                    cmd.angular.z = (
                        -self.turn_speed
                    )

            else:

                cmd.linear.x = (
                    self.forward_speed
                )

                cmd.angular.z = 0.0


        elif self.state == "TURNING_LEFT":

            cmd.linear.x = 0.0

            cmd.angular.z = (
                self.turn_speed
            )

            if (
                front_distance
                > self.clear_distance
            ):

                self.state = "MOVING"

                cmd.linear.x = (
                    self.forward_speed
                )

                cmd.angular.z = 0.0


        elif self.state == "TURNING_RIGHT":

            cmd.linear.x = 0.0

            cmd.angular.z = (
                -self.turn_speed
            )

            if (
                front_distance
                > self.clear_distance
            ):

                self.state = "MOVING"

                cmd.linear.x = (
                    self.forward_speed
                )

                cmd.angular.z = 0.0


        self.cmd_vel_publisher.publish(cmd)


        if (
            self.state
            != self.last_reported_state
        ):

            front_text = (
                f"{front_distance:.2f} m"
                if math.isfinite(
                    front_distance
                )
                else "inf"
            )

            left_text = (
                f"{left_distance:.2f} m"
                if math.isfinite(
                    left_distance
                )
                else "inf"
            )

            right_text = (
                f"{right_distance:.2f} m"
                if math.isfinite(
                    right_distance
                )
                else "inf"
            )

            self.get_logger().info(

                f"{self.state} | "

                f"X: {self.robot_x:.2f} m | "

                f"Y: {self.robot_y:.2f} m | "

                f"Front: {front_text} | "

                f"Left: {left_text} | "

                f"Right: {right_text}"

            )

            self.last_reported_state = (
                self.state
            )


    def stop_robot(self):

        stop_cmd = Twist()

        stop_cmd.linear.x = 0.0

        stop_cmd.angular.z = 0.0

        self.cmd_vel_publisher.publish(
            stop_cmd
        )


def main(args=None):

    rclpy.init(args=args)

    node = ObstacleAvoidance()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        pass

    finally:

        node.stop_robot()

        node.destroy_node()

        rclpy.shutdown()


if __name__ == '__main__':

    main()
