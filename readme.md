# Buddy: ROS 2 Mapping and Autonomous Navigation Simulation

This repository contains the ROS 2 packages, configuration files, and launch scripts for **Buddy**, a custom differential-drive robot simulated in Gazebo. It provides a complete, working pipeline for mapping an unknown environment and executing autonomous, obstacle-avoiding navigation.

---

## 🚀 Project Overview: What Has Been Implemented

This project successfully integrates several complex ROS 2 systems to achieve full autonomy in simulation. 

### 1. Mapping & Localization (SLAM Toolbox)
* **Simulation Bridge:** Connected Gazebo's simulated sensors (LiDAR and wheel encoders) to ROS 2 using `ros_gz_bridge`, ensuring strict simulation time synchronization across all nodes to prevent TF (Transform) tree errors.
* **Real-Time Mapping:** Implemented the `async_slam_toolbox_node` to fuse odometry and laser scan data. This allows the robot to generate a highly accurate 2D occupancy grid (map) of its environment while being driven manually.
* **Map Serialization:** Configured the `nav2_map_server` to permanently save the generated map as a static `.pgm` image and `.yaml` metadata file for future autonomous use.

### 2. Autonomous Navigation & Obstacle Avoidance (Nav2 Stack)
* **Custom Launch Architecture:** Built a streamlined `navigation.launch.py` script that handles the entire Nav2 bringup sequence, utilizing absolute file paths to ensure the map server never fails to load the environment.
* **AMCL Localization:** Deployed Adaptive Monte Carlo Localization to dynamically track the robot's coordinates against the pre-saved map using a particle filter.
* **Dynamic Obstacle Avoidance:** Tuned custom Costmap parameters (`nav2_params.yaml`). Configured the `robot_radius`, `inflation_radius`, and `cost_scaling_factor` to ensure the robot gives wide berths to physical obstacles and walls.
* **Kinematic Tuning:** Optimized the DWB Local Planner to increase the robot's maximum autonomous driving speed (`max_vel_x` and `max_vel_theta`) while respecting the simulated hardware's acceleration limits.

---

## 🛠️ Getting Started (For New Users)

Follow these steps to clone, build, and run the simulation on your local machine.

### Prerequisites
* **OS:** Ubuntu Linux 22.04
* **ROS 2:** Humble Hawksbill
* **Simulator:** Gazebo (Fortress or Harmonic)
* **Required Packages:**
  ```bash
  sudo apt update
  sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-slam-toolbox ros-humble-ros-gz ros-humble-teleop-twist-keyboard
  ```

### 1. Clone and Build the Workspace
Open a terminal and run the following commands to set up the workspace:
```bash
# Create a workspace directory
mkdir -p ~/buddy_ws/src
cd ~/buddy_ws/src

# Clone the repository
git clone [https://github.com/Tamizhanban212/arm_bot_navigation.git](https://github.com/Tamizhanban212/arm_bot_navigation.git) .

# Build the package
cd ~/buddy_ws
colcon build --packages-select buddy_description

# Source the setup file
source install/setup.bash
```

---

## 🗺️ Phase 1: How to Generate a Map (SLAM)

If you want to map the Gazebo world from scratch, follow these steps. **Open a new terminal for each step** and remember to run `cd ~/buddy_ws && source install/setup.bash` in every terminal first!

**1. Launch the Simulation:**
```bash
ros2 launch buddy_description gazebo.launch.py
```

**2. Launch the SLAM Node:**
```bash
ros2 run slam_toolbox async_slam_toolbox_node --ros-args --params-file ./src/buddy_description/config/mapper_params_online_async.yaml -p use_sim_time:=True
```

**3. Launch RViz (Visualization):**
```bash
ros2 run rviz2 rviz2 --ros-args -p use_sim_time:=true
```
*(In RViz, set the Fixed Frame to `map`, and add the `/map` and `/scan` displays).*

**4. Drive the Robot:**
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
Use your keyboard to drive Buddy around until the map in RViz is completely drawn out.

**5. Save the Map:**
Once the map looks good, open one final terminal and save it:
```bash
ros2 run nav2_map_server map_saver_cli -f ~/buddy_ws/src/buddy_description/maps/my_new_map
```

---

## 🧭 Phase 2: How to Navigate Autonomously

Once you have a map, you can tell the robot to drive itself. 

**🚨 CRITICAL SETUP STEP:** The ROS 2 Map Server requires the **absolute path** to the map image. 
1. Open the map config file: `nano ~/buddy_ws/src/buddy_description/maps/my_map.yaml`
2. Change the `image:` path on the very first line to match your computer's username. 
   *(Example: `image: /home/YOUR_USERNAME/buddy_ws/src/buddy_description/maps/my_map.pgm`)*

### Execution Steps
Close all running terminals. Open three new terminals (remembering to source the workspace in each).

**1. Launch the Simulation:**
```bash
ros2 launch buddy_description gazebo.launch.py
```

**2. Launch the Nav2 Stack:**
```bash
ros2 launch buddy_description navigation.launch.py
```

**3. Launch RViz:**
```bash
ros2 run rviz2 rviz2 --ros-args -p use_sim_time:=true
```

### How to Drive in RViz
1. Set the **Fixed Frame** to `map`. Add the `Map` (`/map`), `LaserScan` (`/scan`), and `RobotModel` displays. 
   *(Note: Ensure the Map display's **Durability Policy** is set to `Transient Local` in the topic settings).*
2. **Localize the Robot:** Click the **2D Pose Estimate** button at the top. Click on the map where Buddy is currently sitting in Gazebo and drag the green arrow in the direction it is facing. The full map will instantly appear.
3. **Send a Goal:** Click the **Nav2 Goal** button at the top. Click anywhere in the open space on the map and drag to set the final orientation. Buddy will calculate the path and drive there automatically!