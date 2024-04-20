#!/usr/bin/env python

import rospy
import cv2
from ultralytics import YOLO
from cv_bridge import CvBridge
from sensor_msgs.msg import Image


class VideoSubscriber:
    def __init__(self):
        rospy.init_node("video_subscriber", anonymous=True)

        self.bridge = CvBridge()

        # Load the YOLOv8 model
        model_path = rospy.get_param("nn_model_path")
        self.yolo_model = YOLO(model_path, verbose=True)

        # Subscribe to the video topic
        self.image_sub = rospy.Subscriber("/uav0/camera/image_raw", Image, self.callback)

    def callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            results = self.yolo_model.predict(cv_image, verbose=False)

            annotated_frame = results[0].plot()

            cv2.imshow("Og Stream", cv_image)
            cv2.imshow("Adnotated Stream", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                rospy.signal_shutdown("User pressed 'q'")

        except Exception as e:
            rospy.logerr("Error in ROS Image to OpenCV image callback: %s", e)

    def run(self):
        rospy.spin()


if __name__ == "__main__":
    video_subscriber = VideoSubscriber()
    video_subscriber.run()
    cv2.destroyAllWindows()
