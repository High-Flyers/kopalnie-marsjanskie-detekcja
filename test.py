import cv2
from ultralytics import YOLO
import pyrealsense2 as rs
import numpy as np
import datetime

weights_path = "/home/hf-guest/droniada_2024/kopalnie_marsjanskie/runs/detect/yolo_v8s_e50_b16_/weights/best.pt"

# Initialize your YOLO model
predictor = YOLO(weights_path)

# Configuration for RealSense
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the RealSense pipeline
pipeline.start(config)

# Get the depth sensor's depth scale
profile = pipeline.get_active_profile()
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame or not depth_frame:
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        # Perform prediction on the color frame
        results = predictor(color_image)
        boxes = results[0].boxes.xyxy.tolist()  # Bounding box coordinates
        classes = results[0].boxes.cls.tolist()  # Detected class indices
        names = results[0].names  # Class names
        confidences = results[0].boxes.conf.tolist()  # Confidence scores

        # Draw the predictions on the color frame
        for box, cls, conf in zip(boxes, classes, confidences):
            x1, y1, x2, y2 = map(int, box)  # Convert coordinates to integers
            label = names[int(cls)]  # Get the class name using the class index
            confidence = conf
            text = f'{label}: {confidence:.2f}'

            # Draw rectangle and text
            cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(color_image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Convert depth image to colormap for visualization
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(np.asanyarray(depth_frame.get_data()), alpha=0.03), cv2.COLORMAP_JET)

        # Show images
        cv2.imshow('RealSense Color Frame', color_image)
        cv2.imshow('RealSense Depth Frame', depth_colormap)

        # Break loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Stop streaming
    pipeline.stop()
    # Release recordings
    cv2.destroyAllWindows()
