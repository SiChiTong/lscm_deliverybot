# lscm_deliverybot
## install

    cd lscm_deliverybot
    vcs import .. < my.repos

# :computer: Single deliverybot sim 

## Mapping

    ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py  

![simulation](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/sim.png)

    ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=true
    tel

### save the map

    ros2 run nav2_map_server map_saver_cli -f ~/map

## Navigation
`ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py`  
  
run in workspace  

    ros2 launch demos gui_door_sim.launch.py

![navigation](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/nav.png)  
![sim_graph](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/sim_graph.png) 
![gui](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/gui.png) 
# Single deliverybot real
## Mapping
### :robot: Robot

    ros2 launch deliverybot_bringup bringup.launch.py
    ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=false

### :computer: Laptop

    tel

### :robot:/:computer: save the map

    ros2 run nav2_map_server map_saver_cli -f ~/map

## Navigation
### :robot: Robot

    ros2 launch deliverybot_bringup bringup.launch.py
    ros2 launch turtlebot3_navigation2 navigation2.launch.py

![navigation](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/nav_real.png)  
![real_graph](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/real_graph.png)

### :robot: GUI

    ros2 run simple_nav demo_gui
    
### :computer: Laptop

    ros2 run rviz2 rviz2 -d src/lscm_deliverybot/turtlebot3_navigation2/rviz/nav.rviz

### Services
disable the Motors  
`ros2 service call /disable_motor std_srvs/srv/Trigger`  
enable the Motors  
`ros2 service call /enable_motor std_srvs/srv/Trigger`
