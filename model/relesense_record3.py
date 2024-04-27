import cv2
import pyrealsense2 as rs
import numpy as np
import datetime
import threading
import time
from utils.streamer import Streamer



def get_profiles():
    ctx = rs.context()
    devices = ctx.query_devices()
    color_profiles = []
    depth_profiles = []

    for device in devices:
        name = device.get_info(rs.camera_info.name)
        serial = device.get_info(rs.camera_info.serial_number)
        print('Sensor: {}, {}'.format(name, serial))
        print('Supported video formats:')
        for sensor in device.query_sensors():
            for stream_profile in sensor.get_stream_profiles():
                stream_type = str(stream_profile.stream_type())

                if stream_type in ['stream.color', 'stream.depth']:
                    v_profile = stream_profile.as_video_stream_profile()
                    fmt = stream_profile.format()
                    w, h = v_profile.width(), v_profile.height()
                    fps = v_profile.fps()

                    video_type = stream_type.split('.')[-1]
                    print('  {}: width={}, height={}, fps={}, fmt={}'.format(
                        video_type, w, h, fps, fmt))
                    if video_type == 'color':
                        color_profiles.append((w, h, fps, fmt))
                    else:
                        depth_profiles.append((w, h, fps, fmt))

    return color_profiles, depth_profiles


def handle_input():
    global is_recording, color_out, depth_out, start_time
    while True:
        user_input = input()
        if user_input.lower() == 'r':
            if is_recording:
                is_recording = False
                color_out.release()
                depth_out.release()
                print("Recording stopped.")
            else:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                color_filename = f"color_video_{timestamp}.avi"
                depth_filename = f"depth_video_{timestamp}.avi"

                color_out = cv2.VideoWriter(color_filename, fourcc, 30.0, (1280, 720))
                depth_out = cv2.VideoWriter(depth_filename, fourcc, 30.0, (1280, 720))
                start_time = datetime.datetime.now()
                is_recording = True
                print("Started recording.")

# get_profiles()
# Configuration for RealSense
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30) # for usb 2.0

# Start the RealSense pipeline
pipeline.start(config)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
color_out = None
depth_out = None
is_recording = False
start_time = None
streamer = Streamer(adress="tcp://10.42.0.1:5555", sending_fps=15, jpeg_quality=70)

# Start a thread to handle user input
input_thread = threading.Thread(target=handle_input)
input_thread.daemon = True
input_thread.start()

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        frame_to_send = cv2.resize(color_image, (640, 360))
        streamer.add_frame_to_send(frame_to_send)

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        if is_recording:
            color_out.write(color_image)
            depth_out.write(depth_colormap)

            if (datetime.datetime.now() - start_time).seconds >= 30:
                is_recording = False
                color_out.release()
                depth_out.release()
                print("Recording saved after 30 seconds.")
                
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                color_filename = f"color_video_{timestamp}.avi"
                depth_filename = f"depth_video_{timestamp}.avi"

                color_out = cv2.VideoWriter(color_filename, fourcc, 30.0, (1280, 720))
                depth_out = cv2.VideoWriter(depth_filename, fourcc, 30.0, (1280, 720))
                is_recording = True
                start_time = datetime.datetime.now()
                print("New recording started.")

except KeyboardInterrupt:
    # Clean up on Ctrl+C exit
    pipeline.stop()
    print("Pipeline and video writers closed.")
#
