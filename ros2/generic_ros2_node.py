#!/usr/bin/env python3
"""generic ros2 python node"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class GenericSpinPublisherNode(Node):

  def __init__(self):
    super().__init__('generic_spin_publisher')

    # Create a publisher for a String message on the '/my_topic' topic
    self.publisher_ = self.create_publisher(String, '/my_topic', 10)
    
    # Create a subscription to listen to a different topic '/my_sub_topic'
    self.subscription = self.create_subscription(
        String, '/my_sub_topic', self.listener_callback, 10
    )
    self.subscription  # prevent unused variable warning

    # Set a timer to call the spin/publish logic every 0.5 seconds
    timer_period = 0.5
    self.timer = self.create_timer(timer_period, self.spin_and_publish)
    self.counter = 0

  def spin_and_publish(self):
    """Generic function representing custom 'spin' or work logic."""
    msg = String()
    msg.data = f'Hello ROS 2: message count {self.counter}'
    self.publisher_.publish(msg)
    self.get_logger().info(f'Publishing: "{msg.data}"')
    self.counter += 1

  def listener_callback(self, msg):
    """Callback function triggered whenever a message arrives on the subscribed topic."""
    self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
  rclpy.init(args=args)
  node = GenericSpinPublisherNode()

  try:
    # Standard ROS 2 spin to keep the node processing callbacks and timers
    rclpy.spin(node)
  except KeyboardInterrupt:
    pass
  finally:
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
  main()
