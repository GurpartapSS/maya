from setuptools import setup
import os
import glob
package_name = 'arm_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob.glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='gurpartapsingh.sarkaria@gmail.com',
    description='Control physical bot iki',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'handTrack=arm_controller.handTracking:main',
            'jsMonitor=arm_controller.jointsMonitor:main',
        ],
    },
)
