#!/usr/bin/env python2
from tkinter import *
import customtkinter
from threading import *

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
import tf_transformations
from time import sleep

decoction = [.0, .0 ,0.0]
outpatient = [.0, -1.5 , 0.0]
deliver = [1.0, 4.5 ,1.52]

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
root = customtkinter.CTk()

rclpy.init()
navigator = BasicNavigator()

initial_pose = PoseStamped()

def threading(x,y,th):
    t0=Thread(target=lambda: task(x,y,th))
    t0.start()

def main():
    # Set our demo's initial pose
    
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    q = tf_transformations.quaternion_from_euler(0, 0, 0.0)
    initial_pose.pose.orientation.z = q[2]
    initial_pose.pose.orientation.w = q[3]
    navigator.setInitialPose(initial_pose)

    # Wait for navigation to fully activate
    navigator.waitUntilNav2Active()



    # creating tkinter window
    
    root.geometry("700x350")
    root.configure(background="white")

    # # Adding widgets to the root window
    label = customtkinter.CTkLabel(master=root, text="LSCM Deliverybot", font =('Default', 100))
    label.pack(side = TOP, pady = 80)


    decoction_button = customtkinter.CTkButton(width= 800, master=root, text="DECOCTION", command=lambda: threading(decoction[0],decoction[1], decoction[2]), font=('Default', 80))
    decoction_button.pack(padx=20, pady=20)

    outpatient_button = customtkinter.CTkButton(width= 800, master=root, text="OUTPATIENT", command=lambda: threading(outpatient[0],outpatient[1],outpatient[2]), font=('Default', 80))
    outpatient_button.pack(padx=20, pady=20)

    deliver_button = customtkinter.CTkButton(width= 800, master=root, text="DELIVER", command=lambda: threading(deliver[0],deliver[1],deliver[2]), font=('Default', 80))
    deliver_button.pack(padx=20, pady=20)


    # Exit Button
    # Button(root, text="Exit", font= "none 32",command=close_window, background="white").pack(side = BOTTOM)
    exit_button = customtkinter.CTkButton(master=root, text="Exit/STOP", command=lambda: close_window("exiting"), font=('Default', 60))
    exit_button.pack(padx=20, pady=20,side = BOTTOM)

    root.attributes('-fullscreen',True)
    root.mainloop()

def close_window(string):
    navigator.cancelTask()
    print(string)
    root.destroy()
    exit()

def task(x,y,th):
    navigator.clearLocalCostmap()
    goal = PoseStamped()
    goal.header.frame_id = 'map'
    goal.header.stamp = navigator.get_clock().now().to_msg()
    goal.pose.position.x = x
    goal.pose.position.y = y
    q = tf_transformations.quaternion_from_euler(0, 0, th)
    goal.pose.orientation.z = q[2]
    goal.pose.orientation.w = q[3]
    navigator.goToPose(goal)
    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        print("in progress")

    print("reached goal")
    # sleep(5)

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('complete! Returning to start...')
        # go back to start
        initial_pose.header.stamp = navigator.get_clock().now().to_msg()
        # navigator.goToPose(initial_pose)
    elif result == TaskResult.CANCELED:
        print(f'Task was canceled. Returning to staging point...')
        initial_pose.header.stamp = navigator.get_clock().now().to_msg()
        navigator.goToPose(initial_pose)
    elif result == TaskResult.FAILED:
        print(f'Task failed!')
        exit(-1)

    while not navigator.isTaskComplete():
        pass

    


if __name__ == '__main__':
    main()