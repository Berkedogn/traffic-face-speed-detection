import cv2

def determine_box_color(vehicle_count, low_threshold, medium_threshold):
    if vehicle_count < low_threshold:
        return (102, 204, 0)  # Yeşil
    elif low_threshold <= vehicle_count <= medium_threshold:
        return (204, 204, 0)  # Mavi
    else:
        return (0, 0, 255)  # Kırmızı

def draw_boxes(frame, detected_objects, box_color):
    for obj in detected_objects:
        x1, y1, x2, y2 = map(int, obj['box'])
        cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 1)
        label = f"{obj['class_name']} ({obj['confidence']*100:.1f}%)"
        cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, box_color, 1)

def display_info(frame, vehicle_count, traffic_status):
    cv2.putText(frame, f"Vehicle Count: {vehicle_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
    cv2.putText(frame, traffic_status, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
