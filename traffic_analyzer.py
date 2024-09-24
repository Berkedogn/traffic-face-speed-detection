from ultralytics import YOLO
import logging

class TrafficAnalyzer:
    def __init__(self, model_path, vehicle_classes):
        self.model = YOLO(model_path)
        self.vehicle_classes = vehicle_classes
        self.model_class_names = self.model.names
        logging.info(f"Model loaded: {model_path}")

    def analyze_frame(self, frame):
        results = self.model(frame)
        vehicle_count = 0
        detected_objects = []

        for result in results:
            for i, class_index in enumerate(result.boxes.cls.tolist()):
                class_name = self.model_class_names[int(class_index)]
                if class_name in self.vehicle_classes:
                    vehicle_count += 1
                    detected_objects.append({
                        "class_name": class_name,
                        "box": result.boxes.xyxy[i].tolist(),
                        "confidence": result.boxes.conf[i]
                    })
        
        logging.info(f"Detected {vehicle_count} vehicles.")
        return vehicle_count, detected_objects
