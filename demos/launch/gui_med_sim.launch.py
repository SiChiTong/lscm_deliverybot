from ament_index_python.packages import get_package_share_path
import launch
from launch.actions import IncludeLaunchDescription
import launch_ros.actions


def generate_launch_description():
    return launch.LaunchDescription([
        IncludeLaunchDescription(str(get_package_share_path('turtlebot3_navigation2') / 'launch/navigation2.launch.py'),
                launch_arguments={'use_sim_time': 'true',
                                  "map": str(get_package_share_path('turtlebot3_navigation2') / 'map/house.yaml')
                                  }.items()
                                 ),
        launch_ros.actions.Node(name='simple_nav', package='simple_nav', executable='gui_med_sim'),  
        
        IncludeLaunchDescription(str(get_package_share_path('deliverybot_mqtt') / 'launch/example_string_launch.py'))
                
        
            
    ])