import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 1. Get the path to the official Nav2 bringup package
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    # 2. Build the exact absolute path to your map file
    # This prevents the "install vs src" folder missing file errors
    home_dir = os.path.expanduser('~')
    map_file = os.path.join(home_dir, 'Documents', 'arm_bot_ws', 'src', 'buddy_description', 'maps', 'my_map.yaml')
    config_file = os.path.join(home_dir, 'Documents', 'arm_bot_ws', 'src', 'buddy_description', 'config', 'nav2_params.yaml')

    # 3. Include the Nav2 bringup launch file with our custom arguments
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

    return LaunchDescription([
        nav2_launch
    ])