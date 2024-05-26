from setuptools import setup

package_name = 'arm_ws'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='gurpartapsingh.sarkaria@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'jMonitor = arm_ws.jointsMonitor:main',
            'coordJointClient = arm_ws.coordJointClient:main',
            'handTracking = arm_ws.handTracking:main',
        ],
    },
)
