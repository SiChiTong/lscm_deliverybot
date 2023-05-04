#!/usr/bin/env python3
from websocket import create_connection
import json
import rospy
from std_msgs.msg import Int16

class ComLift:
    def __init__(self):
        rospy.init_node('tko_lift')
        self.url = 'ws://192.168.1.185:1234/ws'
        self.data_1 = {'device_id':'0', 'action': 'click', 'floor': '0'}
        self.data_5 = {'device_id':'0', 'action': 'click', 'floor': '5'}
        self.data_loc = {'device_id':'0', 'action': 'location'}
        self.sub_lift_check = rospy.Subscriber("lift_cmd_check", Int16, self.lift_task_check, queue_size=1)
        self.sub_lift = rospy.Subscriber("lift_cmd", Int16, self.lift_task, queue_size=1)
        # lift door reached
        self.pub_lift_reached = rospy.Publisher('lift_reached', Int16, queue_size=1)
        self.pub_lift_check = rospy.Publisher('lift_cmd_check_status', Int16, queue_size=1)

    def lift_task(self, msg):
        ws = create_connection(self.url)
        print("connected")
        if msg.data==1:
            ws.send(json.dumps(self.data_1))
            print("sending lift goal 1")
        elif msg.data==5:
            ws.send(json.dumps(self.data_5))
            print("sending lift goal 5")
        ws.close()
        print("lift sending connection closed")

    def lift_task_check(self, msg):
        ws = create_connection(self.url)
        print("connected")
        while True:        
            print("checking lift floors")
            ws.send(json.dumps(self.data_loc))
            tmp = ws.recv()
            feedback = list(tmp.split("\""))
            print(feedback[11])
            print(feedback)
            self.pub_lift_check.publish(int(feedback[11]))
            if feedback[11] == '5' and feedback[15] == 'arriveok':
                self.pub_lift_reached.publish(1)
                break
            rospy.sleep(2)
        ws.close()
        print("lift checking connection closed")

if __name__ == '__main__':
    test = ComLift()
    rospy.spin()
