# lscm_deliverybot
`git clone --recurse-submodules git@github.com:JosefGst/lscm_deliverybot.git`

## Single deliverybot
`roslaunch sim_world hospital.launch model:=deliverybot`  
![alt text](https://github.com/JosefGst/lscm_deliverybot/blob/main/images/single_hospital.png)  

`roslaunch deliverybot_nav navigation.launch model:=deliverybot`  
![alt text](https://github.com/JosefGst/lscm_deliverybot/blob/main/images/single_deliverybot.png)  



## Multiple deliverybots Simulation
`roslaunch sim_world multi_hospital.launch`  
![alt text](https://github.com/JosefGst/lscm_deliverybot/blob/main/images/multi_hospital.png)

`roslaunch deliverybot_nav multi_nav_bringup.launch`  
![alt text](https://github.com/JosefGst/lscm_deliverybot/blob/main/images/multi_deliverybot.png)


## Multiple deliverybots real

### Laptop
`git clone --recurse-submodules git@github.com:JosefGst/lscm_deliverybot.git`

`roscore`  
![](https://github.com/JosefGst/lscm_deliverybot/blob/main/images/split_screen_delivery.gif)

### Robot1
use branch **robot1**  
`git clone --recurse-submodules git@github.com:JosefGst/lscm_deliverybot.git -b robot1`

source deliverybot_ws  
`roslaunch deliverybot_bringup bringup_multi.launch`

### Robot2
use branch **robot2** "TODO"  
source deliverybot_ws 
`roslaunch deliverybot_bringup bringup_multi.launch`

### Robot3
use branch **robot3** "TODO"  
`git clone --recurse-submodules git@github.com:JosefGst/lscm_deliverybot.git -b robot3`

source deliverybot_ws  
`roslaunch deliverybot_bringup bringup_multi.launch`

### Laptop
source deliverybot_ws  
`roslaunch deliverybot_nav multi_nav_bringup.launch map_name:=ros_map12_mod`

## Resources
[R2D2 sounds](https://www.soundboard.com/sb/r2d2_r2_d2_sounds)
