import time

class SpeedDetector:
    def __init__(self, line1_y, line2_y, fps, distance_between_lines):
        self.line1_y = line1_y
        self.line2_y = line2_y
        self.fps = fps
        self.distance_between_lines = distance_between_lines
        self.vehicle_times = {}  # Araçların çizgiyi geçme zamanları
        self.vehicle_speeds = {}  # Araçların hızları

    def calculate_speed(self, vehicle_id, vehicle_center_y):
        current_time = time.time()
        
        if vehicle_id not in self.vehicle_times:
            self.vehicle_times[vehicle_id] = (vehicle_center_y, current_time)  # İlk geçiş kaydı
            return None

        previous_y, previous_time = self.vehicle_times[vehicle_id]

        # Eğer araç çizgiyi geçtiyse
        if previous_y < self.line1_y <= vehicle_center_y or previous_y < self.line2_y <= vehicle_center_y:
            time_taken = current_time - previous_time
            speed = (self.distance_between_lines / time_taken) * 3.6  # m/s'den km/h'ye çevir
            
            # Hızın mantıklı bir değerde olup olmadığını kontrol et
            if speed < 0 or speed > 200:  # Örneğin, 0 ile 200 km/h arasında bir hız kabul edelim
                speed = None
            else:
                self.vehicle_speeds[vehicle_id] = speed  # Hızı kaydet
            
            # Yeni kaydı güncelle
            self.vehicle_times[vehicle_id] = (vehicle_center_y, current_time)
            return speed

        return None
