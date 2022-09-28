#!/usr/bin/env python2
from Tkinter import *
from send_goal import *
import time

i = 0

rospy.init_node("gui_send_goal")
# creating tkinter window
root = Tk()
root.geometry("700x350")
root.configure(background="white")

# Adding widgets to the root window
Label(root, text = 'LSCM Deliverybot',bg="white", font =(
'Verdana', 32)).pack(side = TOP, pady = 10)

# Creating a photoimage object to use image
photo = PhotoImage(file = "/home/lscm/deliverybot_ws/src/lscm_deliverybot/medical_task/include/startnext.png")
photoimage = photo.subsample(1,1)


def close_window():
    root.destroy()
    exit()


def send_goal():
    global i
    if i == 0: # got to deliver 
        rospy.sleep(1)
        door_control("123,2,3000") # close
        time.sleep(1)
        movebase_client(13.5, 0.40, 1.5) # rotate to goal
        movebase_client(14.7, 5, 3.15) # go to deliver
        door_control("123,1,3000") # open
        # rospy.sleep(10)
        # door_control("123,2,3000") # close
        # movebase_client(16, -.5, 3.14) # come home
        # door_control("123,1,3000") # open
        i = 1
    else: # go to kitchen
        rospy.sleep(1)
        door_control("123,2,3000") # close
        time.sleep(1)
        movebase_client(14.7, 5, -1.5) # rotate to goal
        movebase_client(13.5, 0.40, 3.15) # go to deliver
        door_control("123,1,3000") # open
        i = 0


# set image on button
Button(root, image=photoimage,command=send_goal, background="white").place(relx=.5, rely=.5,anchor= CENTER)

Button(root, text="Exit", font= "none 32",command=close_window, background="white").pack(side = BOTTOM)

root.attributes('-fullscreen',True)
mainloop()
