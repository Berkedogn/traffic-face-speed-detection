import logging
import cv2
from config import CONFIG
from video_processor import VideoProcessor
from traffic_analyzer import TrafficAnalyzer
from drawing_utils import determine_box_color, draw_boxes, display_info
from traffic_status import get_traffic_status
from face_blurring import FaceBlurrer
from speed_detector import SpeedDetector
from lane_tracker import LaneTracker

logging.basicConfig(level=logging.INFO)

def main():
    # Video ve model işlemleri
    video_processor = VideoProcessor(CONFIG['video_path'], CONFIG['output_path'], CONFIG['codec'], CONFIG['fps'])
    traffic_analyzer = TrafficAnalyzer(CONFIG['model_path'], CONFIG['vehicle_classes'])
    face_blurrer = FaceBlurrer("yolov8l_100e.pt")  # Yüz tespit modeli

    # Hız tespiti ve şerit takibi için modüllerin başlatılması
    speed_detector = SpeedDetector(CONFIG['line1_y'], CONFIG['line2_y'], CONFIG['fps'], 20)  # 2 çizgi arası mesafe 20 metre
    lane_tracker = LaneTracker([(0, 200), (200, 400), (400, 600)])  # Şerit sınırları

    # Araç durumunu izlemek için bir sözlük
    vehicle_speed_tracking = {}

    # Ana döngü
    while True:
        ret, frame = video_processor.read_frame()
        if not ret:
            break

        # Araç tespiti
        vehicle_count, detected_objects = traffic_analyzer.analyze_frame(frame)

        # Trafik durumu belirleme ve kutu rengi
        traffic_status = get_traffic_status(vehicle_count, CONFIG['low_traffic_threshold'], CONFIG['medium_traffic_threshold'])
        box_color = determine_box_color(vehicle_count, CONFIG['low_traffic_threshold'], CONFIG['medium_traffic_threshold'])

        # Araç kutularını çiz ve bilgileri göster
        draw_boxes(frame, detected_objects, box_color)
        display_info(frame, vehicle_count, traffic_status)

        # Hız ve şerit tespiti
        for vehicle_id, vehicle in enumerate(detected_objects):
            if len(vehicle['box']) == 4:  # box uzunluğunu kontrol et
                vehicle_center_y = (vehicle['box'][1] + vehicle['box'][3]) / 2
                vehicle_center_x = (vehicle['box'][0] + vehicle['box'][2]) / 2
                
                # Hız hesaplama
                speed = speed_detector.calculate_speed(vehicle_id, vehicle_center_y)

                # Araç yeşil çizgiye değdi mi?
                if speed is not None:
                    # Hızı yalnızca yeşil çizgiye değdiğinde göster
                    cv2.putText(frame, f"Speed: {speed:.2f} km/h", 
                                (int(vehicle['box'][0]), int(vehicle['box'][1] - 15)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

                # Şerit bilgisi
                lane = lane_tracker.get_lane(vehicle_center_x)
                if lane is not None:  # lane None değilse
                    cv2.putText(frame, f"Lane: {lane}", 
                                (int(vehicle['box'][0]), int(vehicle['box'][1] - 30)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Çizgileri çiz
        cv2.line(frame, (0, CONFIG['line1_y']), (frame.shape[1], CONFIG['line1_y']), (0, 255, 0), 2)  # Yeşil çizgi
        cv2.line(frame, (0, CONFIG['line2_y']), (frame.shape[1], CONFIG['line2_y']), (0, 0, 255), 2)  # Kırmızı çizgi

        # Yüz bulanıklaştırma işlemi
        frame = face_blurrer.blur_faces(frame)

        # Çıktı frame'i kaydet
        video_processor.write_frame(frame)

    # Kaynakları serbest bırak
    video_processor.release_resources()

if __name__ == "__main__":
    main() 
