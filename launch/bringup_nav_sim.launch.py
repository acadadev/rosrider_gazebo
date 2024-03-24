import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition, UnlessCondition

ROBOT_MODEL = os.environ['ROBOT_MODEL']

'''
   launches localization, navigation, with given map, and parameters for robot, for simulation
'''


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='True')

    # notice map:=map_file_full_pathname loads different map
    map_file = LaunchConfiguration('map', default=os.path.join(get_package_share_directory('rosrider_navigation2'), 'map', 'willow.yaml'))

    nav2_param_file = LaunchConfiguration('params_file', default=os.path.join(get_package_share_directory('rosrider_navigation2'), 'param', 'nav2_params_' + ROBOT_MODEL + '.yaml'))
    nav2_launch_dir = os.path.join(get_package_share_directory('nav2_bringup'), 'launch')
    rviz_config_file = os.path.join(get_package_share_directory('rosrider_navigation2'), 'rviz', 'rosrider_navigation2.rviz')

    return LaunchDescription([
        DeclareLaunchArgument('map', default_value=map_file, description='full path to map file'),
        DeclareLaunchArgument('params_file', default_value=nav2_param_file, description='full path to param file'),
        DeclareLaunchArgument('use_sim_time', default_value='True', description='use simulation time if true'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_launch_dir, '/bringup_launch.py']),
            launch_arguments={'map': map_file, 'use_sim_time': use_sim_time, 'params_file': nav2_param_file}.items(),
        ),
        Node(
             package='rviz2',
             executable='rviz2',
             name='rviz2',
             arguments=['-d', rviz_config_file],
             parameters=[{'use_sim_time': use_sim_time}],
             condition=IfCondition(LaunchConfiguration('launch_rviz', default='True')),
             output='screen')
    ])
