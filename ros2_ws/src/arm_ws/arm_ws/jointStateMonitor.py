import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from collections import deque
import time
import sys
import threading

sys.path.append('/home/ubuntu/autoBot')

from armControl.armDriver2 import armDriver
class MinimalSubscriber(Node):

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
                dutycycles = self.q.popleft()
                self.q.clear()
                self.get_logger().info('Moving!')
                for i, joints in enumerate(dutycycles):
                    print(i,joints)
                self.ad.set_jointStates(dutycycles)
                self.get_logger().info('Moved!')
        #at this points remove all other entries from queue


    def listener_callback(self, msg):
        current_time = time.time()
        if(current_time - self.start_time < 1):
            return
        # self.get_logger().info('time passed')
        self.start_time = current_time
        joint_positions = [round(x,2) for x in msg.position]
        if(self.starterFlag == 0):
            self.cachedJoints = joint_positions
            self.starterFlag = 1
        all_equal = all(x == y for x, y in zip(joint_positions, self.cachedJoints))
        if(all_equal):
            return
        self.cachedJoints = joint_positions
        print(self.cachedJoints)
        print(joint_positions)
        with self.lock:
            selected_joints = joint_positions[:3]+[joint_positions[4]]
            self.q.appendleft(selected_joints)
            self.get_logger().info('Appening jointStates: "%f"' % self.cachedJoints[1])


def main(args=None):
    rclpy.init(args=args)

    jointStates_subscriber = MinimalSubscriber()
    rclpy.spin(jointStates_subscriber)
    jointStates_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()