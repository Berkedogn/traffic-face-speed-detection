import cv2
from ultralytics import YOLO
import logging

class FaceBlurrer:
    def __init__(self, face_model_path):
        self.face_model = YOLO(face_model_path)
        logging.info(f"Face detection model loaded: {face_model_path}")

    def blur_faces(self, frame):
        results = self.face_model(frame)
        for result in results:
            for box in result.boxes:
                # Elde edilen box bilgileri
                xyxy = box.xyxy[0]
                x1 = int(xyxy[0])
                y1 = int(xyxy[1])
                x2 = int(xyxy[2])
                y2 = int(xyxy[3])

                # Yüz bölgesini tespit et ve bulanıklaştır
                face = frame[y1:y2, x1:x2]
                blurred_face = cv2.GaussianBlur(face, (161, 161), 30)

                # Orijinal frame'e bulanık yüzü ekle
                frame[y1:y2, x1:x2] = blurred_face

                logging.info(f"Face blurred at coordinates: ({x1}, {y1}, {x2}, {y2})")
        return frame
