from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    mode_arg = DeclareLaunchArgument(
        'mode',
        default_value='0',
        description='Mode to run the node: 0 for JointStateMonitor, 1 for JointsController, 2 for HandTrackingNode'
    )

    mode = LaunchConfiguration('mode')

    joint_state_monitor_node = Node(
        package='arm_controller',
        executable='jsMonitor',
        name='joint_state_monitor',
        output='screen',
        parameters=[],
        arguments=['0']
    )

    joints_controller_node = Node(
        package='arm_controller',
        executable='jsMonitor',
        name='joints_controller',
        output='screen',
        parameters=[],
        arguments=['1']
    )

    hand_tracking_node = Node(
        package='arm_controller',
        executable='handTrack',
        name='hand_tracking_node',
        output='screen'
    )

    return LaunchDescription([
        mode_arg,
        joint_state_monitor_node if mode == '0' else joints_controller_node,
        hand_tracking_node
    ])
