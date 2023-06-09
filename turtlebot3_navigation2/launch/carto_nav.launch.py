# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Darby Lim

import os

from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_package_share_path
import launch_ros.actions
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    map_dir = LaunchConfiguration(
        'map',
        default=os.path.join(
            get_package_share_directory('turtlebot3_navigation2'),
            'map',
            'lab.yaml'))
    
    laser_filter = LaunchConfiguration(
        'laser_filter_params',
        default=os.path.join(
            get_package_share_directory('turtlebot3_navigation2'),
            'param',
            'laser_filter.yaml'))

    param_file_name = TURTLEBOT3_MODEL + '_carto.yaml'
    param_dir = LaunchConfiguration(
        'params_file',
        default=os.path.join(
            get_package_share_directory('turtlebot3_navigation2'),
            'param',
            param_file_name))

    nav2_launch_file_dir = os.path.join(get_package_share_directory('nav2_bringup'), 'launch')
    carto_launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_cartographer'), 'launch')

    rviz_config_dir = os.path.join(
        get_package_share_directory('turtlebot3_navigation2'),
        'rviz',
        'nav.rviz')
    
    use_respawn = LaunchConfiguration('use_respawn')

    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value=map_dir,
            description='Full path to map file to load'),

        DeclareLaunchArgument(
            'params_file',
            default_value=param_dir,
            description='Full path to param file to load'),

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        DeclareLaunchArgument(
            'use_respawn', default_value='False',
            description='Whether to respawn if a node crashes. Applied when composition is disabled.'),

        Node(
            package="laser_filters",
            executable="scan_to_scan_filter_chain",
            # name="laser_filter_front",
            parameters=[laser_filter, {'use_sim_time': LaunchConfiguration('use_sim_time')}],
            # remappings=[
                # ('/scan', '/scan_front'),
                # ('/scan_filtered', '/scan_filtered_front'),
            # ]
        ),

        # Node(
        #     package="laser_filters",
        #     executable="scan_to_scan_filter_chain",
        #     namespace="back",
        #     parameters=[laser_filter, {'use_sim_time': LaunchConfiguration('use_sim_time')}],
        #     remappings=[
        #         ('/scan', '/scan_back'),
        #         ('/scan_filtered', '/scan_filtered_back'),
        #     ]
        # ),

        # Node(
        #     package='robot_localization',
        #     executable='ekf_node',
        #     name='ekf_filter_node',
        #     output='screen',
        #     parameters=[os.path.join(get_package_share_directory('turtlebot3_navigation2'), 'param/ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}]
        # ),

        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([carto_launch_file_dir, '/cartographer_localization.launch.py']),
        #     launch_arguments={
        #         'use_sim_time': use_sim_time,
        #         'params_file': param_dir}.items(),
        # ),
        
        # launch_ros.actions.Node(name='map_server', package='nav2_map_server', executable='map_server', output='screen' , respawn=use_respawn, respawn_delay=2.0,),


        IncludeLaunchDescription(str(get_package_share_path('turtlebot3_cartographer') / 'launch/cartographer_localization.launch.py'),
                                 launch_arguments={'use_sim_time': use_sim_time}.items()),

        IncludeLaunchDescription(str(get_package_share_path('nav2_bringup') / 'launch/navigation_launch.py'),
                                 launch_arguments={'use_sim_time': use_sim_time}.items()),

        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([nav2_launch_file_dir, '/bringup_launch.py']),
        #     launch_arguments={
        #         'map': map_dir,
        #         'use_sim_time': use_sim_time,
        #         'params_file': param_dir}.items(),
        # ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),
    ])
