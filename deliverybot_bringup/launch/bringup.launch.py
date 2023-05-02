import os

from ament_index_python.packages import get_package_share_directory

import launch
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import GroupAction, DeclareLaunchArgument
from launch_ros.actions import PushRosNamespace
from launch.substitutions import LaunchConfiguration, TextSubstitution
from ament_index_python.packages import get_package_share_path

def generate_launch_description():
   return launch.LaunchDescription([

      # RPLIDAR
      IncludeLaunchDescription(str(get_package_share_path('rplidar_ros2') / 'launch/rplidar_s1_launch.py'),
                              launch_arguments={
                              'serial_port': '/dev/rplidar_front',
                              'frame_id': 'front_scan',
                              }.items()),
      # ZLAC
      IncludeLaunchDescription(str(get_package_share_path('ros_zlac_8015_driver') / 'zlac.launch.py')),
      # STATE PUBLISHER
      IncludeLaunchDescription(str(get_package_share_path('deliverybot_bringup') / 'launch/turtlebot3_state_publisher.launch.py')),
      # MPU6050 IMU
      IncludeLaunchDescription(str(get_package_share_path('mpu6050driver') / 'launch/mpu6050driver_launch.py')),

   ])