import os

from ament_index_python.packages import get_package_share_directory
import launch
import launch_ros
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition
from launch.actions import DeclareLaunchArgument, ExecuteProcess


def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='deliverybot_navigation').find('deliverybot_navigation')
    slam_param_name = 'slam_params_file'
    slam_config_path = PathJoinSubstitution(
        [FindPackageShare('deliverybot_navigation'), 'config', 'slam.yaml']
    )
    slam_launch_path = PathJoinSubstitution(
        [FindPackageShare('slam_toolbox'), 'launch', 'online_async_launch.py']
    )
    rviz_config_path = PathJoinSubstitution(
        [FindPackageShare('deliverybot_navigation'), 'rviz', 'slam.rviz']
    )

    sim_world = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('sim_world'), 'launch'),
         '/house.launch.py'])
    )
    robot_localization_node = launch_ros.actions.Node(
         package='robot_localization',
         executable='ekf_node',
         name='ekf_filter_node',
         output='screen',
         parameters=[os.path.join(pkg_share, 'config/ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )
    slam_toolbox = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(slam_launch_path),
            launch_arguments={
                'use_sim_time': LaunchConfiguration("use_sim_time"),
                slam_param_name: slam_config_path
            }.items()
    )
    laser_filter = Node(
            package="laser_filters",
            executable="scan_to_scan_filter_chain",
            parameters=[
                PathJoinSubstitution([
                    get_package_share_directory("deliverybot_navigation"),
                    "config", "laser_filter.yaml",
                ])],
        )
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path],
        condition=IfCondition(LaunchConfiguration("rviz")),
        parameters=[{'use_sim_time': LaunchConfiguration("use_sim_time")}]
    )
   

    return LaunchDescription([
        DeclareLaunchArgument(name='rviz', default_value='true', 
                                            description='Run rviz'),
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=rviz_config_path,
                                            description='Absolute path to rviz config file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time'),
        sim_world,
        robot_localization_node,
        slam_toolbox,
        laser_filter,
        rviz_node
    ])