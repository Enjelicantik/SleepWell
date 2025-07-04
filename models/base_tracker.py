from abc import ABC, abstractmethod
import json
import os

class BaseTracker(ABC):
    """Abstract base class for all tracker types"""
    
    def __init__(self):
        self.data_file = None
    
    @abstractmethod
    def get_sleep_statistics(self):
        """Get sleep statistics - must be implemented by subclasses"""
        pass
    
    def save_data(self):
        """Save data to JSON file"""
        if not self.data_file:
            return
        
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load data from JSON file"""
        if not self.data_file or not os.path.exists(self.data_file):
            return None
        
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def to_dict(self):
        """Convert to dictionary - should be overridden by subclasses"""
        return {}
    
    @classmethod
    def from_dict(cls, data):
        """Create instance from dictionary - should be overridden by subclasses"""
        return cls()
    
    def validate_skin_condition(self, condition):
        """Validate skin condition input"""
        valid_conditions = ['kering', 'normal', 'berjerawat']
        return condition.lower() in valid_conditions
    
    def format_duration(self, hours, minutes):
        """Format duration for display"""
        if hours == 0:
            return f"{minutes}m"
        elif minutes == 0:
            return f"{hours}h"
        else:
            return f"{hours}h {minutes}m"