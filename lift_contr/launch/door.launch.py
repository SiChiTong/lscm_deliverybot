import launch
import launch_ros.actions


def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(name='lift', package='lift_contr', executable='lift_door', namespace='lift',
                                parameters=[{'address': 'F5:EC:6E:A0:BF:CD',
                                            'uuid': '34860001-E699-4650-ae12-f1f3c8bf9ad9'}]),

        launch_ros.actions.Node(name='tko_door', package='lift_contr', executable='lift_door', namespace='tko_door',
                                parameters=[{'address': 'E3:59:A8:08:10:F7',
                                            'uuid': '34860001-e699-4650-ae12-f1f3c8bf9ad9'}]),
    
    ])