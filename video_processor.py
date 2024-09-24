import cv2
import logging

class VideoProcessor:
    def __init__(self, video_path, output_path, codec, fps):
        self.cap = cv2.VideoCapture(video_path)
        fourcc = cv2.VideoWriter_fourcc(*codec)
        self.out = cv2.VideoWriter(output_path, fourcc, fps, (int(self.cap.get(3)), int(self.cap.get(4))))
        logging.info(f"Video initialized: {video_path}")

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            logging.warning("End of video or cannot read frame.")
        return ret, frame

    def write_frame(self, frame):
        self.out.write(frame)

    def release_resources(self):
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()
        logging.info("Resources released.")
