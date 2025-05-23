from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    ekf_params = {
        'frequency': 30.0,
        'sensor_timeout': 0.1,
        'two_d_mode': False,

        'imu0': 'imu/data',
        'imu0_config': [False, False, False,
                        True, True, True,
                        False, False, False,
                        True, True, True],
        'imu0_queue_size': 10,
        'imu0_differential': False,
        'imu0_remove_gravitational_acceleration': True,

        'odom0': 'odometry/gps',
        'odom0_config': [True, True, False,
                         False, False, False,
                         False, False, False,
                         False, False, False],
        'odom0_queue_size': 5,

        'process_noise_covariance': [
            0.05, 0, 0, 0, 0, 0,
            0, 0.05, 0, 0, 0, 0,
            0, 0, 0.05, 0, 0, 0,
            0, 0, 0, 0.05, 0, 0,
            0, 0, 0, 0, 0.05, 0,
            0, 0, 0, 0, 0, 0.05,
        ],
    }

    navsat_transform_params = {
        'frequency': 30.0,
        'magnetic_declination_radians': 0.0,
        'yaw_offset': 0.0,
        'zero_altitude': False,
        'wait_for_datum': False,
        'broadcast_utm_transform': True,
        'publish_filtered_gps': True,
        'transform_time_offset': 0.0,
        'yaw_threshold': 0.3490658504,  # 20 degrees
    }

    return LaunchDescription([

        # EKF node
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[ekf_params],
            remappings=[
                ('imu/data', 'imu/data'),
                ('odometry/filtered', 'odometry/filtered'),
            ],
        ),

        # NavSat transform node
        Node(
            package='robot_localization',
            executable='navsat_transform_node',
            name='navsat_transform',
            output='screen',
            parameters=[navsat_transform_params],
            arguments = ['--ros-args', '--log-level', 'debug'],
            remappings=[
                ('imu', 'imu/data'),
                ('gps/fix', 'gps/fix'),
                ('gps/filtered', 'gps/filtered'),
                ('odometry/gps', 'odometry/gps'),
            ],
        ),

        # Fake IMU node
        Node(
            package='fake_imu_publisher',
            executable='fake_imu_publisher_node',
            name='fake_imu',
            output='screen'
        ),
    ])
