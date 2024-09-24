class LaneTracker:
    def __init__(self, lane_boundaries):
        self.lane_boundaries = lane_boundaries  # Şerit sınırları [(x1_left, x1_right), (x2_left, x2_right)]

    def get_lane(self, vehicle_x_center):
        for i, (left, right) in enumerate(self.lane_boundaries):
            if left <= vehicle_x_center <= right:
                return i + 1  # Şerit numarasını döndür
        return None
