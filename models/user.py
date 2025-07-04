from datetime import datetime
from .sleep_record import SleepRecord
from .base_tracker import BaseTracker

class User(BaseTracker):
    """User class that inherits from BaseTracker"""
    
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.sleep_records = []
        self.current_sleep_session = None
        self.reminder_time = "21:00"
        
    def start_sleep(self, skin_condition):
        """Start a new sleep session"""
        if self.current_sleep_session:
            return False  # Already has active session
        
        sleep_record = SleepRecord(
            sleep_time=datetime.now(),
            skin_before=skin_condition
        )
        
        self.current_sleep_session = sleep_record
        self.sleep_records.append(sleep_record)
        self.save_data()
        return True
    
    def wake_up(self, skin_condition):
        """End current sleep session"""
        if not self.current_sleep_session:
            return None
        
        self.current_sleep_session.end_sleep(skin_condition)
        result = {
            'duration_hours': self.current_sleep_session.duration_hours,
            'duration_minutes': self.current_sleep_session.duration_minutes
        }
        
        self.current_sleep_session = None
        self.save_data()
        return result
    
    def get_sleep_statistics(self):
        """Get sleep statistics - implements abstract method"""
        if not self.sleep_records:
            return {
                'total_records': 0,
                'average_duration': 0,
                'short_sleep_count': 0
            }
        
        completed_records = [r for r in self.sleep_records if r.wake_time]
        total_duration = sum(r.duration_hours + r.duration_minutes/60 for r in completed_records)
        short_sleep_count = len([r for r in completed_records if r.duration_hours < 6])
        
        return {
            'total_records': len(completed_records),
            'average_duration': total_duration / len(completed_records) if completed_records else 0,
            'short_sleep_count': short_sleep_count
        }
    
    def get_skin_condition_analysis(self):
        """Analyze skin condition patterns"""
        if not self.sleep_records:
            return {}
        
        completed_records = [r for r in self.sleep_records if r.wake_time]
        skin_conditions = {}
        
        for record in completed_records:
            before = record.skin_before
            after = record.skin_after
            
            if before not in skin_conditions:
                skin_conditions[before] = {'improved': 0, 'same': 0, 'worsened': 0}
            
            if after == before:
                skin_conditions[before]['same'] += 1
            elif (before == 'berjerawat' and after in ['normal', 'kering']) or \
                 (before == 'kering' and after == 'normal'):
                skin_conditions[before]['improved'] += 1
            else:
                skin_conditions[before]['worsened'] += 1
        
        return skin_conditions
    
    def to_dict(self):
        """Convert user data to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'reminder_time': self.reminder_time,
            'sleep_records': [record.to_dict() for record in self.sleep_records],
            'current_sleep_session': self.current_sleep_session.to_dict() if self.current_sleep_session else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create User instance from dictionary"""
        user = cls(data['name'])
        user.reminder_time = data.get('reminder_time', '21:00')
        
        # Load sleep records
        user.sleep_records = [SleepRecord.from_dict(record_data) 
                             for record_data in data.get('sleep_records', [])]
        
        # Load current session if exists
        if data.get('current_sleep_session'):
            user.current_sleep_session = SleepRecord.from_dict(data['current_sleep_session'])
        
        return user
    
    def is_sleeping(self):
        """Return True if there is an active sleep session."""
        return self.current_sleep_session is not None