from ultralytics import YOLO
from PIL import Image
import cv2

weights_path = "model/runs/detect/yolo_v8s_e50_b16_/weights/best.pt"


# Load the YOLOv8 model
model = YOLO(weights_path)

# Open the video file
# video_path = 0
video_path = "model/test_video.avi"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        cv2.imshow("Frame", frame)
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
