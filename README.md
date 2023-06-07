# lscm_deliverybot
Is ad differential drive robot based on the turtlebot to do indoor delivery tasks.

## install
    
    cd lscm_deliverybot
    sudo apt install python3-vcstool
    vcs import .. < my.repos
    roscd # cd to root of ros workspace
    rosdep update && rosdep install -i --from-path src --rosdistro $ROS_DISTRO -y
    cd src/ros_zlac_8015_driver
    git submodule init
    git submodule update

install zlac motor driver

    pip3 install pymodbus
    pip3 install serial_asyncio
    sudo python3 setup.py install
    sudo usermod -a -G dialout $USER

    
# :computer: deliverybot Simulation 

## Mapping

    ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py  

![simulation](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/sim.png)

    ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=true
&#13;

    tel

### save the map

    ros2 run nav2_map_server map_saver_cli -f ~/map

## Navigation
run in workspace  

    ros2 launch turtlebot3_navigation2 navigation2.launch.py map:=src/lscm_deliverybot/turtlebot3_navigation2/map/house.yaml

![navigation](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/nav.png)  
![sim_graph](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/sim_graph.png) 
### Demos
#### taking lift
    ros2 launch demos gui_door_sim.launch.py

![gui](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/gui.png) 

#### MQTT publisher

    docker run --rm --network host --name mosquitto eclipse-mosquitto

to publish the messages on localhost, change the IP in deliverybot_mqtt/config/params.ros2.yaml to localhost
```yaml
mqtt_location:
    ros__parameters:
        broker:
        host: localhost
        port: 1883
        bridge:
        ros2mqtt:
            ros_topic: /robots/id_1/location
            mqtt_topic: robots/id_1/location
            primitive: true
```

    ros2 launch demos gui_med_sim.launch.py 

---
# :robot: Real deliverybot 
## Mapping
### :robot: Robot

    ros2 launch deliverybot_bringup bringup.launch.py
&#13;

    ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=false
&#13;

    ros2 run rviz2 rviz2 -d src/lscm_deliverybot/turtlebot3_cartographer/rviz/tb3_cartographer.rviz

### :computer: Laptop

    tel

### :robot:/:computer: save the map

    ros2 run nav2_map_server map_saver_cli -f ~/map

## Navigation
### :robot: Robot

    ros2 launch deliverybot_bringup bringup.launch.py
&#13;

    ros2 launch turtlebot3_navigation2 navigation2.launch.py map:=src/lscm_deliverybot/turtlebot3_navigation2/map/lab_tko4.yaml

### :computer: Laptop

    ros2 run rviz2 rviz2 -d src/lscm_deliverybot/turtlebot3_navigation2/rviz/nav.rviz

![navigation](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/nav_real.png)  
![real_graph](https://github.com/JosefGst/lscm_deliverybot/blob/humble/images/real_graph.png)

### :robot: Demos
launch the bringup manually first. For some timing issue it cant be put in the same launch file yet.

    ros2 launch deliverybot_bringup bringup.launch.py
&#13;

    ros2 launch demos gui_door.launch.py
  
&#13;
or

    ros2 launch demos gui_med.launch.py


### :robot: start MQTT client

    ros2 launch deliverybot_mqtt example_string_launch.py
    


### Services
disable the Motors  
`ros2 service call /disable_motor std_srvs/srv/Trigger`  
enable the Motors  
`ros2 service call /enable_motor std_srvs/srv/Trigger`
