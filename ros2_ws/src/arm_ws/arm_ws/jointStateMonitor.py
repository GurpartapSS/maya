import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

import time

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('jointStates_subscriber')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10)
        self.subscription
        self.start_time = time.time()
        self.starterFlag = 0
        self.cachedJoints = []
        # Make object of arm driver

    def listener_callback(self, msg):
        current_time = time.time()
        if(current_time - self.start_time < 1):
            return
        self.get_logger().info('time passed')
        self.start_time = current_time
        joint_positions = [round(x,4) for x in msg.position]
        if(self.starterFlag == 0):
            self.cachedJoints = joint_positions
            self.starterFlag = 1
        all_equal = all(x == y for x, y in zip(joint_positions, self.cachedJoints))
        if(all_equal):
            return
        self.cachedJoints = joint_positions
        self.get_logger().info('I heard a change: "%f"' % self.cachedJoints[1])

        #Call Arm movement with latest


def main(args=None):
    rclpy.init(args=args)

    jointStates_subscriber = MinimalSubscriber()

    rclpy.spin(jointStates_subscriber)
    jointStates_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()