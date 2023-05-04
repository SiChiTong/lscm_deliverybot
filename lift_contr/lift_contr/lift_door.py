from std_srvs.srv import SetBool

import rclpy
from rclpy.node import Node

from lift_contr.submodules import bt_door_contr

class DoorService(Node, bt_door_contr.BtDoor):

    def __init__(self):
        super().__init__('door_service')

        self.declare_parameter('address', rclpy.Parameter.Type.STRING)
        self.declare_parameter('uuid', rclpy.Parameter.Type.STRING)
        # get parameters
        address = self.get_parameter('address').value
        uuid = self.get_parameter('uuid').value

        self.srv = self.create_service(SetBool, 'door_control', self.door_cb)
        self.lift = bt_door_contr.BtDoor(address,uuid)  

    def door_cb(self, request, response):
        self.get_logger().info('Incoming request\nbool: %d' % (request.data))
        if request.data == self.lift.CLOSE:
            self.lift.control(self.lift.CLOSE)
            response.message= 'door closed'
            response.success = True
            return response
        elif request.data == self.lift.OPEN:
            self.lift.control(self.lift.OPEN)
            response.message= 'door opened'
            response.success = True
            return response
        else:
            response.success = False
            return response
        response.success = False
        return response


def main(args=None):
    rclpy.init(args=args)
    door_service = DoorService()
    rclpy.spin(door_service)
    rclpy.shutdown()


if __name__ == '__main__':
    main()