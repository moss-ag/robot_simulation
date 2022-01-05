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
python3 create_farm.py -nb 2 -nr 4 3 -ntr 4 5
```
Make sure to edit the `declare_world_path` variable in `simulation.launch.py` file to the desired file path.

## Launching the simulation
Execute this to launch the full simulation with RViz, navigation and loacalization.
```
ros2 launch spraybot_bringup simulation.launch.py  
```

Only Gazebo Sim
TODO

