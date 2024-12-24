import cv2
import threading
import time

class IPCamera(threading.Thread):
    def __init__(self, rtsp_url, name):
        threading.Thread.__init__(self)
        self.rtsp_url = rtsp_url
        self.name = name
        self.frame = None
        self.stopped = False

    def run(self):
        cap = cv2.VideoCapture(self.rtsp_url)
        while not self.stopped:
            ret, self.frame = cap.read()
            if not ret:
                print(f"Error: Could not connect to the camera {self.name}")
                break
            time.sleep(0.01)  # Small delay to reduce CPU usage
        cap.release()

    def stop(self):
        self.stopped = True

# List of RTSP URLs
rtsp_urls = [
    "rtsp://admin:WBK191124@172.23.253.42:554/Streaming/Channels/101",
    "rtsp://admin:PTL_ct_2024@172.23.253.43:554/Streaming/Channels/101",
    # Add more RTSP URLs as needed
    # RTSP URL of Hikvision camera "rtsp://<username>:<password>@<ip_address>:<port>/Streaming/Channels/101"
    # where "101" stands for the main channel, 102 the sub-channel
]


# Create and start camera threads
cameras = []
for i, url in enumerate(rtsp_urls):
    camera = IPCamera(url, f"Camera_{i+1}")
    camera.start()
    cameras.append(camera)

try:
    while True:
        frames = []
        for camera in cameras:
            if camera.frame is not None:
                frame = cv2.resize(camera.frame, (640, 360))
                frames.append(frame)

        if frames:
            # Combine frames horizontally
            combined_frame = cv2.hconcat(frames)
            cv2.imshow('Multiple IP Cameras', combined_frame)

        # Exit by pressing "ESC"
        if cv2.waitKey(1) == 27:
            break

finally:
    # Stop all camera threads
    for camera in cameras:
        camera.stop()

    # Wait for all threads to finish
    for camera in cameras:
        camera.join()

    cv2.destroyAllWindows()
