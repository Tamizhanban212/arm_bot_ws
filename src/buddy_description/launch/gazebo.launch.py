import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_share = get_package_share_directory('buddy_description')
    
    urdf_file = os.path.join(pkg_share, 'urdf', 'buddy.urdf')
    robot_description_config = xacro.process_file(urdf_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}]
    )

    # Path to your custom world
    world_path = os.path.join(pkg_share, 'urdf', 'world.sdf')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': '/home/tamizhanbanag/Documents/arm_bot_ws/src/buddy_description/urdf/world.sdf'}.items(),
    )

    # Spawn Buddy in the corner (-4, -4)
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'buddy',
                   '-x', '-4.0', 
                   '-y', '-4.0', 
                   '-z', '0.05'], # 5cm drop is safer than 0 to avoid physics glitches
        output='screen'
    )

    # Bridge ROS topics and Ignition topics
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
            # THIS LINE ADDS ODOM TO THE TF TREE
            '/model/buddy/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'
        ],
        # Remap the Ignition topic to the standard ROS /tf topic
        remappings=[('/model/buddy/tf', '/tf')],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        gazebo,
        spawn_entity,
        bridge
    ])