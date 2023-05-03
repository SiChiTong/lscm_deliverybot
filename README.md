# lscm_deliverybot
## install

    cd lscm_deliverybot
    vcs import .. < my.repos

# Single deliverybot sim
`ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py`  
![simulation](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/sim.png)  

run in workspace  
`ros2 launch turtlebot3_navigation2 navigation2.launch.py map:=src/lscm_deliverybot/turtlebot3_navigation2/map/house.yaml use_sim_time:=true`  
![navigation](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/nav.png)  
![sim_graph](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/sim_graph.png)

run simple commander in simulator 
`ros2 run simple_nav demo_inspection`  
`ros2 run simple_nav demo_security`
## GUI  
    
    ros2 run simple_nav demo_gui_sim
    
![gui](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/gui.png) 
# Single deliverybot real
## :robot: Robot

    ros2 launch deliverybot_bringup bringup.launch.py
    ros2 launch turtlebot3_navigation2 navigation2.launch.py

![navigation](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/nav_real.png)  
![real_graph](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/real_graph.png)

    ros2 run simple_nav demo_gui
    
## :computer: Laptop

    ros2 run rviz2 rviz2 -d src/lscm_deliverybot/turtlebot3_navigation2/rviz/nav.rviz
### Services
disable the Motors  
`ros2 service call /disable_motor std_srvs/srv/Trigger`  
enable the Motors  
`ros2 service call /enable_motor std_srvs/srv/Trigger`
