import sys
import termios
import tty
import time
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class WASDController(Node):
    def __init__(self):
        super().__init__('wasd_controller')

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

    def send_cmd(self, linear_x=0.0, angular_z=0.0):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.publisher.publish(msg)

    def rotate_360(self):
        msg = Twist()

        angular_speed = 1.57
        duration = 2 * math.pi / angular_speed

        msg.linear.x = 0.0
        msg.angular.z = angular_speed

        start_time = time.time()

        while time.time() - start_time < duration:
            self.publisher.publish(msg)
            time.sleep(0.05)

        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher.publish(msg)


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(
            fd,
            termios.TCSADRAIN,
            old_settings
        )

    return key


def main():
    rclpy.init()
    node = WASDController()

    print("===== Turtle Controller =====")
    print("W : Forward")
    print("S : Backward")
    print("A : Turn Left")
    print("D : Turn Right")
    print("R : Rotate 360 degrees")
    print("X : Stop")
    print("Q : Quit")
    print("=============================")

    while True:
        key = get_key().lower()

        if key == 'w':
            print("Forward")
            node.send_cmd(2.0, 0.0)

        elif key == 's':
            print("Backward")
            node.send_cmd(-2.0, 0.0)

        elif key == 'a':
            print("Turn Left")
            node.send_cmd(0.0, 2.0)

        elif key == 'd':
            print("Turn Right")
            node.send_cmd(0.0, -2.0)

        elif key == 'r':
            print("Rotate 360 degrees")
            node.rotate_360()

        elif key == 'x':
            print("Stop")
            node.send_cmd(0.0, 0.0)

        elif key == 'q':
            print("Quit")
            node.send_cmd(0.0, 0.0)
            break

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
