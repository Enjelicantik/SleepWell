from datetime import datetime

class SleepRecord:
    """Class to represent a single sleep record"""
    
    def __init__(self, sleep_time, skin_before, wake_time=None, skin_after=None):
        self.sleep_time = sleep_time
        self.skin_before = skin_before
        self.wake_time = wake_time
        self.skin_after = skin_after
        self.duration_hours = 0
        self.duration_minutes = 0
        
        if wake_time:
            self.calculate_duration()
    
    def end_sleep(self, skin_after):
        """End the sleep session"""
        self.wake_time = datetime.now()
        self.skin_after = skin_after
        self.calculate_duration()
    
    def calculate_duration(self):
        """Calculate sleep duration"""
        if self.wake_time and self.sleep_time:
            duration = self.wake_time - self.sleep_time
            total_minutes = int(duration.total_seconds() // 60)
            self.duration_hours = total_minutes // 60
            self.duration_minutes = total_minutes % 60
    
    def is_short_sleep(self):
        """Check if sleep duration is less than 6 hours"""
        return self.duration_hours < 6
    
    def get_sleep_quality(self):
        """Determine sleep quality based on duration"""
        if self.duration_hours >= 8:
            return "Excellent"
        elif self.duration_hours >= 7:
            return "Good"
        elif self.duration_hours >= 6:
            return "Fair"
        else:
            return "Poor"
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'sleep_time': self.sleep_time.isoformat(),
            'skin_before': self.skin_before,
            'wake_time': self.wake_time.isoformat() if self.wake_time else None,
            'skin_after': self.skin_after,
            'duration_hours': self.duration_hours,
            'duration_minutes': self.duration_minutes
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create SleepRecord from dictionary"""
        sleep_time = datetime.fromisoformat(data['sleep_time'])
        wake_time = datetime.fromisoformat(data['wake_time']) if data['wake_time'] else None
        
        record = cls(
            sleep_time=sleep_time,
            skin_before=data['skin_before'],
            wake_time=wake_time,
            skin_after=data.get('skin_after')
        )
        
        record.duration_hours = data.get('duration_hours', 0)
        record.duration_minutes = data.get('duration_minutes', 0)
        
        return record