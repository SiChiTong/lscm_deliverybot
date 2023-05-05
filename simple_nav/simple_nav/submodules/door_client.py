import sys

from std_srvs.srv import SetBool
import rclpy
from rclpy.node import Node


class DoorClientAsync(Node):
    def __init__(self):
        super().__init__("door_client_async")
        self.cli = self.create_client(SetBool, "/lift/door_control")
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        self.req = SetBool.Request()

    def send_request(self, cmd):
        self.req.data = bool(cmd)
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)

    door_client = DoorClientAsync()
    response = door_client.send_request(int(sys.argv[1]))
    print(response.message)

    door_client.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
