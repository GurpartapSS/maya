import rclpy
from rclpy.node import Node
from inverse_kine.srv import XyzToJoints


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(XyzToJoints, 'xyz_to_joints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = XyzToJoints.Request()

    def send_request(self, h, y, d):
        self.get_logger().info('SENDING REQUEST')
        self.req.h = h
        self.req.y = y
        self.req.d = d
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClientAsync()
    response = minimal_client.send_request(12.0, 4.0, 12.0)
    minimal_client.get_logger().info(
        'Result of Joints: %f %f %f %f' %
        (response.joints[0], response.joints[1], response.joints[2], response.joints[3]))
    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
