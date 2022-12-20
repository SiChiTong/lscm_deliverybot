#!/usr/bin/env python2
from tkinter import *
import customtkinter
from threading import *

from copy import deepcopy

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
import tf_transformations
from time import sleep


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
root = customtkinter.CTk()

rclpy.init()
navigator = BasicNavigator()

initial_pose = PoseStamped()

def threading():
    # Call work function
    # t1=Thread(target=send_goal1)
    t0=Thread(target=task)
    # t1.start()
    t0.start()

def main():
    # Set our demo's initial pose
    
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.pose.position.x = -1.2
    initial_pose.pose.position.y = 1.25
    q = tf_transformations.quaternion_from_euler(0, 0, 0.6)
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

    # Creating a photoimage object to use image
    photo = PhotoImage(file = "/home/u/ros2/deliverybot2_ws/src/lscm_deliverybot/simple_nav/images/startnext.png")
    photoimage = photo.subsample(1,1)


    # Start Button
    # customtkinter.CTkButton(root, image=photoimage,command=threading, background="white").place(relx=.5, rely=.5,anchor= CENTER)
    start_button = customtkinter.CTkButton(width= 800, master=root, text="START", command=threading, font=('Default', 80))
    start_button.pack(padx=20, pady=20)

    kitchen_button = customtkinter.CTkButton(width= 800, master=root, text="KITCHEN", command=threading, font=('Default', 80))
    kitchen_button.pack(padx=20, pady=20)

    meeting_button = customtkinter.CTkButton(width= 800, master=root, text="MEETING ROOM", command=threading, font=('Default', 80))
    meeting_button.pack(padx=20, pady=20)


    # Exit Button
    # Button(root, text="Exit", font= "none 32",command=close_window, background="white").pack(side = BOTTOM)
    start_button = customtkinter.CTkButton(master=root, text="Exit/STOP", command=close_window, font=('Default', 60))
    start_button.pack(padx=20, pady=20,side = BOTTOM)

    root.attributes('-fullscreen',True)
    root.mainloop()

def close_window():
    navigator.cancelTask()
    root.destroy()
    exit()

def task():
    navigator.clearLocalCostmap()
    inspection_pose = PoseStamped()
    inspection_pose.header.frame_id = 'map'
    inspection_pose.header.stamp = navigator.get_clock().now().to_msg()
    inspection_pose.pose.position.x = -1.3
    inspection_pose.pose.position.y = 4.0
    q = tf_transformations.quaternion_from_euler(0, 0, 0.6)
    inspection_pose.pose.orientation.z = q[2]
    inspection_pose.pose.orientation.w = q[3]
    navigator.goToPose(inspection_pose)
    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        print("in progress")

    print("reached goal")
    sleep(5)

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Inspection of shelves complete! Returning to start...')
        # go back to start
        initial_pose.header.stamp = navigator.get_clock().now().to_msg()
        navigator.goToPose(initial_pose)
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