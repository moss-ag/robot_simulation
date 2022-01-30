# Spraybot Gazebo Simulation

## Clone
Clone the package into the ```src``` folder of a ROS2 workspace.

## Generate Trees in world
Navigate to the `scripts` directory in `spraybot_simulation` and execute
```
python3 create_farm.py -nb num of blocks -nr num of rows per block (one or more integers) -ntr num of trees per row in each block (one or more integers) -f file path
```

Example command
```
python3 create_farm.py -nb 5 -nr 4 -ntr 6 -f ../worlds/spraybot.world
```
Or 
```
python3 create_farm.py -nb 5 -nr 4 4 5 5 5 -ntr 6 6 7 7 7 -f ../worlds/spraybot.world
```
Where: 
first & second blocks have 4 rows per block and 6 trees in each row
third, forth & fifth blocks have 5 rows per block and 7 trees in each row

Make sure to edit the `declare_world_path` variable in `simulation.launch.py` file to the desired file path.

## Launching the simulation
Execute this to launch the full simulation with RViz, navigation and loacalization.
```
ros2 launch spraybot_bringup simulation.launch.py
```

Refer: https://docs.google.com/document/d/1zr_KFhjDdrWiT50Gsbopc0Ot9QNOyAVU5Y1utftmqac/edit?usp=sharing for setting additional parameters. 

## Waypoint Generation 

The .csv file is opened in append mode, hence delete/rename the .csv before generating new set of points. 
Waypoint generation supported only in: slope, gaussian noise and staggered mode. Does not work if block offset is given.
Supports only: same number of trees and rows per block. See example below 

Example command
```
python3 create_farm.py -nb 5 -nr 4 -ntr 6 -f ../worlds/spraybot.world ../
``` 

Only Gazebo Sim
TODO


