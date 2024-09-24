CONFIG = {
    "video_path": "trafik.mp4",
    "output_path": "output_trafik.avi",
    "codec": "XVID",
    "fps": 30.0,
    "model_path": "yolov8n.pt",
    "vehicle_classes": ['car', 'motorcycle', 'bicycle', 'bus', 'truck'],
    "low_traffic_threshold": 5,
    "medium_traffic_threshold": 10,
    "line1_y": 100,  # İlk çizgi için Y koordinatı
    "line2_y": 300,  # İkinci çizgi için Y koordinatı
    "distance_between_lines": 50  # Çizgiler arasındaki mesafe
}
