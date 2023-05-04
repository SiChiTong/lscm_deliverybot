import launch
import launch_ros.actions


def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(name='list', package='lift_contr', executable='lift_door'),
    ])