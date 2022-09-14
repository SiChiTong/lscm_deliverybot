# lscm_deliverybot

## Single deliverybot
`roslaunch sim_world hospital.launch model:=deliverybot`  
![alt text](https://github.com/JosefGst/lscm_deliverybot/blob/main/images/multi_hospital.png)  
`roslaunch deliverybot_nav navigation.launch model:=deliverybot`  




## Multiple deliverybots Simulation
`roslaunch sim_world multi_hospital.launch`  
![alt text](https://github.com/JosefGst/lscm_deliverybot/blob/main/images/multi_hospital.png)

`roslaunch deliverybot_nav multi_nav_bringup.launch`  


## Multiple deliverybots real
### Laptop
`roscore`  
setup all robots using the laptops ros_master_uri
### Robot1


### Robot2
source medical_ws  
`roslaunch whbot_bringup bringup_multi.launch`

### Laptop
`roslaunch deliverybot_nav multi_nav_bringup.launch map_name:=ros_map12_mod`