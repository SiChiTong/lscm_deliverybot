#!/usr/bin/env python

import rospy
import sys
import tf_conversions
import actionlib
from std_srvs.srv import Empty
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String

global dbot_deliver, change_map, el_open_door, el_close_door, el_change_floor, clear_costmap

def movebase_client(x, y, a):
	
	client = actionlib.SimpleActionClient('/robot1/move_base', MoveBaseAction)
	client.wait_for_server()

	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = "map"
	goal.target_pose.header.stamp = rospy.Time.now()

	goal.target_pose.pose.position.x = x
	goal.target_pose.pose.position.y = y
	goal.target_pose.pose.position.z = 0.0

	quat = tf_conversions.transformations.quaternion_from_euler(
		0.0,
		0.0,
		a
	)

	goal.target_pose.pose.orientation.x = quat[0]
	goal.target_pose.pose.orientation.y = quat[1]
	goal.target_pose.pose.orientation.z = quat[2]
	goal.target_pose.pose.orientation.w = quat[3]
	
	client.send_goal(goal)
	wait = client.wait_for_result()
	rospy.loginfo("Sent Goal")
	if not wait:
		client.cancel_goal()
		rospy.logerr("Action server not available!")
		rospy.signal_shutdown("Action server not available!")
	else:
		return client.get_result()

def door_control(msg):
	pub = rospy.Publisher('/robot1/stm32_door_control', String, queue_size=1)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		for i in range(2):
			rospy.loginfo(msg)
			pub.publish(msg)
			rate.sleep()
		break

def execute_delivery():
	clear_costmap.call()
	while not rospy.is_shutdown():
		rospy.sleep(15)	
		door_control("123,2,3000") # close
		movebase_client(35.5, 37, 0) # EL out
		door_control("123,1,3000") #open
		rospy.sleep(15)
		movebase_client(30.5, 28, 0) # EL out
	return True

		
if __name__ == "__main__":
	rospy.init_node("movebase_client_py")
	clear_costmap = rospy.ServiceProxy('/robot1/move_base/clear_costmaps', Empty)
	result = execute_delivery()
