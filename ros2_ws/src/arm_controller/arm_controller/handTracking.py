import cv2
import mediapipe as mp
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import Float32MultiArray
import time
import sys
import threading

sys.path.append('/home/ubuntu/maya')

from armControl.armDriver2 import armDriver

class HandTrackingNode(Node):
    def __init__(self):
        super().__init__('hand_tracking_node')
        self.publisher_ = self.create_publisher(Image, 'hand_tracking_frames', 10)
        self.msg = [0.0,0.0]
        self.publisherPoints_ = self.create_publisher(Float32MultiArray, 'hand_center', 10)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 128)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 128)
        self.bridge = CvBridge()
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.coord_err = 0.1
        self.get_logger().info('Hand Tracking Node has been started.')

    def timer_callback(self):
        success, frame = self.cap.read()
        if not success:
            self.get_logger().error('Failed to capture frame')
            return
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        msg = Float32MultiArray()
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks_px = np.array([(int(l.x * frame.shape[1]), int(l.y * frame.shape[0])) for l in hand_landmarks.landmark])
                bbox = cv2.boundingRect(landmarks_px)
                x, y, w, h = bbox
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                center_x = x + w // 2
                center_y = y + h // 2
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            msg.data = [float(center_x),float(center_y)]
            if(abs(hand_landmarks.landmark[0].y-hand_landmarks.landmark[12].y) > 0.25):
                msg.data.append(0)
            else:
                msg.data.append(1)
            if(len(msg.data)>0):
                if(abs(center_x - 64) >8 or abs(center_y - 64) > 8):
                    self.publisherPoints_.publish(msg)
        image_message = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        self.publisher_.publish(image_message)
        # cv2.imshow('Hand Tracking', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     rclpy.shutdown()

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

def main(args=None):
    rclpy.init(args=args)
    node = HandTrackingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
