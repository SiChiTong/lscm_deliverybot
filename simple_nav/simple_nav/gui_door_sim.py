#!/usr/bin/env python3

from tkinter import *
import customtkinter
from threading import *

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
import tf_transformations
from time import sleep

from simple_nav.submodules.door_client import DoorClientAsync

sofa = [-1.3, 4.0, 0.6]
kitchen = [-3.0, 0.5, 0.3]
meeting = [-1.3, 4.0, 0.3]

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: blue (default), dark-blue, green
root = customtkinter.CTk()

rclpy.init()
navigator = BasicNavigator()

# door service client
door_client = DoorClientAsync()
OPEN = 1
CLOSE = 0

initial_pose = PoseStamped()


def threading(x, y, th):
    t0 = Thread(target=lambda: task(x, y, th))
    t0.start()


def main():
    # Set our demo's initial pose

    initial_pose.header.frame_id = "map"
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.pose.position.x = -1.2
    initial_pose.pose.position.y = 1.25
    q = tf_transformations.quaternion_from_euler(0, 0, 0.3)
    initial_pose.pose.orientation.z = q[2]
    initial_pose.pose.orientation.w = q[3]
    navigator.setInitialPose(initial_pose)

    # Wait for navigation to fully activate
    navigator.waitUntilNav2Active()

    # creating tkinter window

    root.geometry("700x350")
    root.configure(background="white")

    # # Adding widgets to the root window
    label = customtkinter.CTkLabel(
        master=root, text="LSCM Deliverybot", font=("Default", 100)
    )
    label.pack(side=TOP, pady=80)

    # Start Button
    # customtkinter.CTkButton(root, image=photoimage,command=threading, background="white").place(relx=.5, rely=.5,anchor= CENTER)
    sofa_button = customtkinter.CTkButton(
        width=800,
        master=root,
        text="SOFA",
        command=lambda: threading(sofa[0], sofa[1], sofa[2]),
        font=("Default", 80),
    )
    sofa_button.pack(padx=20, pady=20)

    kitchen_button = customtkinter.CTkButton(
        width=800,
        master=root,
        text="KITCHEN",
        command=lambda: threading(kitchen[0], kitchen[1], kitchen[2]),
        font=("Default", 80),
    )
    kitchen_button.pack(padx=20, pady=20)

    meeting_button = customtkinter.CTkButton(
        width=800,
        master=root,
        text="MEETING ROOM",
        command=lambda: threading(meeting[0], meeting[1], meeting[2]),
        font=("Default", 80),
    )
    meeting_button.pack(padx=20, pady=20)

    # Exit Button
    # Button(root, text="Exit", font= "none 32",command=close_window, background="white").pack(side = BOTTOM)
    exit_button = customtkinter.CTkButton(
        master=root,
        text="Exit/STOP",
        command=lambda: close_window("exiting"),
        font=("Default", 60),
    )
    exit_button.pack(padx=20, pady=20, side=BOTTOM)

    root.attributes("-fullscreen", True)
    root.mainloop()


def close_window(string):
    navigator.cancelTask()
    print(string)
    root.destroy()
    exit()


def task(x, y, th):
    navigator.clearLocalCostmap()
    goal = PoseStamped()
    goal.header.frame_id = "map"
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
    response = door_client.send_request(int(OPEN))
    print(response.message)
    sleep(5)

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print("complete! Returning to start...")
        # go back to start
        initial_pose.header.stamp = navigator.get_clock().now().to_msg()
        navigator.goToPose(initial_pose)
    elif result == TaskResult.CANCELED:
        print(f"Task was canceled. Returning to staging point...")
        initial_pose.header.stamp = navigator.get_clock().now().to_msg()
        navigator.goToPose(initial_pose)
    elif result == TaskResult.FAILED:
        print(f"Task failed!")
        exit(-1)

    while not navigator.isTaskComplete():
        pass
    response = door_client.send_request(int(CLOSE))
    print(response.message)


if __name__ == "__main__":
    main()
