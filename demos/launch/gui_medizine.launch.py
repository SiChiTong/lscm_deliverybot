from ament_index_python.packages import get_package_share_path
import launch
from launch.actions import IncludeLaunchDescription
import launch_ros.actions


def generate_launch_description():
    return launch.LaunchDescription([
        # IncludeLaunchDescription(str(get_package_share_path('deliverybot_bringup') / 'launch/bringup.launch.py'),
        #         launch_arguments={'use_sim_time': 'false'}.items()
        #                          ),
        IncludeLaunchDescription(str(get_package_share_path('turtlebot3_navigation2') / 'launch/navigation2.launch.py'),
                launch_arguments={"map": str(get_package_share_path('turtlebot3_navigation2') / 'map/lab_tko4.yaml')}.items()
                                 ),
        IncludeLaunchDescription(str(get_package_share_path('deliverybot_mqtt') / 'launch/example_string.launch.py'),
                                 ), 
        launch_ros.actions.Node(name='simple_nav', package='simple_nav', executable='gui_door')     
            
    ])