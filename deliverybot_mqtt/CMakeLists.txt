cmake_minimum_required(VERSION 3.8)
project(deliverybot_mqtt)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(mqtt_client REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(deliverybot_mqtt_interfaces REQUIRED)
# find_package(rosidl_default_generators REQUIRED)

# rosidl_generate_interfaces(${PROJECT_NAME}
#   "msg/Configuration.msg"
#   "msg/LocationEntry.msg"
#   "msg/Location.msg"
#   "msg/Status.msg"
#   DEPENDENCIES 
#   geometry_msgs 
#   std_msgs 
#   rosidl_default_generators
# )

add_executable(mqtt_pub src/mqtt_pub.cpp)
ament_target_dependencies(mqtt_pub rclcpp geometry_msgs deliverybot_mqtt_interfaces)

add_executable(mqtt_pub_string src/mqtt_pub_string.cpp)
ament_target_dependencies(mqtt_pub_string rclcpp geometry_msgs deliverybot_mqtt_interfaces)

install(TARGETS
  mqtt_pub
  mqtt_pub_string
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}/
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
