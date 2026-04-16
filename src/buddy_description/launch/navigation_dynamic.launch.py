import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    home_dir = os.path.expanduser('~')
    
    # 1. Point to your map
    map_file = os.path.join(home_dir, 'Documents', 'arm_bot_ws', 'src', 'buddy_description', 'maps', 'my_map.yaml')
    
    # 2. Point to your NEW DYNAMIC config file
    config_file = os.path.join(home_dir, 'Documents', 'arm_bot_ws', 'src', 'buddy_description', 'config', 'nav2_dynamic_params.yaml')

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_file,
            'use_sim_time': 'true',
            'params_file': config_file
        }.items()
    )

    return LaunchDescription([nav2_launch])