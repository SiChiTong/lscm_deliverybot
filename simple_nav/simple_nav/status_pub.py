import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from deliverybot_mqtt_interfaces.msg import Status


class StatusPublisher(Node):

    def __init__(self):
        super().__init__('status_publisher')
        self.publisher_ = self.create_publisher(Status, 'status', 10)

    def pub_status(self, status, from_loc_ic, to_loc_id):
        msg = Status()
        msg.status = status
        msg.from_location_id = from_loc_ic
        msg.to_location_id = to_loc_id
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.status)
        self.get_logger().info('Publishing: "%d"' % msg.from_location_id)
        self.get_logger().info('Publishing: "%d"' % msg.to_location_id)


def main(args=None):
    rclpy.init(args=args)

    status_publisher = StatusPublisher()
    status_publisher.pub_status('DELIVERING',1,2)
    rclpy.spin(status_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    status_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()