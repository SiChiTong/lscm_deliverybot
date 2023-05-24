from ament_index_python.packages import get_package_share_path
import launch
import launch_ros.actions


def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(name='mqtt_node', package='deliverybot_mqtt', executable='mqtt_pub',
                                parameters=[
                                    str(get_package_share_path('deliverybot_mqtt') / 'config/example.yaml')]),
        launch_ros.actions.Node(name='mqtt_configuration', package='mqtt_client', executable='mqtt_client',
                                parameters=[
                                    str(get_package_share_path('deliverybot_mqtt') / 'config/params.ros2.yaml')]),
        launch_ros.actions.Node(name='mqtt_status', package='mqtt_client', executable='mqtt_client',
                                parameters=[
                                    str(get_package_share_path('deliverybot_mqtt') / 'config/params.ros2.yaml')]),
        launch_ros.actions.Node(name='mqtt_location', package='mqtt_client', executable='mqtt_client',
                                parameters=[
                                    str(get_package_share_path('deliverybot_mqtt') / 'config/params.ros2.yaml')]),
    ])