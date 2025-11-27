# setpoint_publisher.py - simple ROS2 publisher (rclpy)
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

class SetpointPub(Node):
    def __init__(self):
        super().__init__('setpoint_pub')
        self.pub = self.create_publisher(PoseStamped, '/mavros/setpoint_position/local', 10)
        self.timer = self.create_timer(0.5, self.timer_cb)
        self.seq = 0

    def timer_cb(self):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'
        msg.pose.position.x = 0.0
        msg.pose.position.y = self.seq * 0.5
        msg.pose.position.z = 10.0
        self.pub.publish(msg)
        self.seq += 1

def main(args=None):
    rclpy.init(args=args)
    node = SetpointPub()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
