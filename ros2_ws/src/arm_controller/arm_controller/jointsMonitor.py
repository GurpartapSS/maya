import rclpy
from rclpy.node import Node
from inverse_kine.msg import JointsRad
from sensor_msgs.msg import JointState
from collections import deque
import time
import sys
import threading

sys.path.append('/home/ubuntu/maya')

from armControl.armDriver2 import armDriver
class JointStateMonitor(Node):

    def __init__(self):
        super().__init__('jointStates_subscriber')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10)
        self.lock = threading.Lock()
        self.q = deque()
        self.subscription
        self.start_time = time.time()
        self.starterFlag = 0
        self.cachedJoints = []
        self.moving = 0
        self.ad = armDriver()

        self.timer = self.create_timer(3, self.timercallback) 
    
    def timercallback(self):
        #lock the queue at this moment
        with self.lock:  # Acquire the lock
            if self.q:
                positions, names = self.q.popleft()
                print(names)
                self.q.clear()
                self.get_logger().info('Moving!')
                self.ad.set_jointStates(0, positions, names)
                self.get_logger().info('Moved!')
        #at this points remove all other entries from queue


    def listener_callback(self, msg):
        current_time = time.time()
        if(current_time - self.start_time < 1):
            return
        self.start_time = current_time
        joint_positions = [round(x,2) for x in msg.position]
        if(self.starterFlag == 0):
            self.cachedJoints = joint_positions
            self.starterFlag = 1
        all_equal = all(x == y for x, y in zip(joint_positions, self.cachedJoints))
        if(all_equal):
            return
        self.cachedJoints = joint_positions
        with self.lock:
            self.q.appendleft((joint_positions[:5],msg.name[:5]))

class JointsController(Node):

    def __init__(self):
        super().__init__('jointStates_subscriber')
        self.subscription = self.create_subscription(
            JointsRad,
            '/joint_rad',
            self.listener_callback,
            10)
        self.lock = threading.Lock()
        self.q = deque()
        self.subscription
        self.starterFlag = 0
        self.cachedJoints = []
        self.moving = 0
        self.ad = armDriver()
        self.timer = self.create_timer(3, self.timercallback) 
        self.get_logger().info('Joints Controller created')
    
    def timercallback(self):
        #lock the queue at this moment
        with self.lock:  # Acquire the lock
            if self.q:
                dutycycles = self.q.popleft()
                self.q.clear()
                self.get_logger().info('Moving!')
                for i, joints in enumerate(dutycycles):
                    print(i,joints)
                self.ad.set_jointStates(1, dutycycles)
                self.get_logger().info('Moved!')
        #at this points remove all other entries from queue


    def listener_callback(self, msg):
        self.get_logger().info('Got new message')
        joint_positions = [round(x,2) for x in msg.joints]
        print(joint_positions)
        with self.lock:
            self.q.appendleft(joint_positions)
            self.get_logger().info('Appening jointStates: "%f"' % joint_positions[1])


def main(args=None):
    rclpy.init(args=args)
    if len(sys.argv) < 2:
        print("Usage: ros2 run arm_controller JsMonitor <joint_name>")
        return
    print(f"Usage: ros2 run arm_controller JsMonitor {sys.argv[1]}")
    if(int(sys.argv[1]) == 0):
        joints_subscriber = JointStateMonitor()
    else:
        joints_subscriber = JointsController()

    rclpy.spin(joints_subscriber)
    joints_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()