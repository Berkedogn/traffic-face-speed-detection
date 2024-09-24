def get_traffic_status(vehicle_count, low_threshold, medium_threshold):
    if vehicle_count < low_threshold:
        return "Traffic: Low"
    elif low_threshold <= vehicle_count <= medium_threshold:
        return "Traffic: Medium"
    else:
        return "Traffic: High"
