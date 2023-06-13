#!/bin/bash

# run inside the shell dir
# . save_map.sh <mapname>
ros2 service call /finish_trajectory cartographer_ros_msgs/srv/FinishTrajectory trajectory_id:\ 0\ 
ros2 service call /write_state cartographer_ros_msgs/srv/WriteState filename:\ \'$HOME/maps/$1.pbstream\' 
ros2 run cartographer_ros cartographer_pbstream_to_ros_map -map_filestem=${HOME}/maps/$1 -pbstream_filename=${HOME}/maps/$1.pbstream -resolution=0.05

# ROS 1
# rosservice call /finish_trajectory 0
# rosservice call /write_state "filename: '${HOME}/maps/$1.pbstream'"
# rosrun cartographer_ros cartographer_pbstream_to_ros_map -map_filestem=${HOME}/maps/$1 -pbstream_filename=${HOME}/maps/$1.pbstream -resolution=0.05