
from models.sleep_tracker import SleepTracker

class Reminder(SleepTracker):
    def __init__(self, ideal_hour):
        super().__init__()
        self.ideal_hour = ideal_hour

    def check_reminder(self, current_hour):
        if current_hour >= self.ideal_hour:
            return "Sudah waktunya tidur!"
        else:
            return "Masih ada waktu, tapi persiapkan untuk tidur."
