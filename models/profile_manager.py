import json
import os
from .user import User

class ProfileManager:
    """Manages user profiles and data persistence"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.profiles_file = os.path.join(data_dir, "profiles.json")
        self.users = {}
        self.load_all_profiles()
    
    def create_profile(self, name):
        """Create a new user profile"""
        if name in self.users:
            return False
        
        user = User(name)
        user.data_file = os.path.join(self.data_dir, f"{name}.json")
        self.users[name] = user
        self.save_profiles_index()
        user.save_data()
        return True
    
    def get_profile(self, name):
        """Get user profile by name"""
        return self.users.get(name)
    
    def get_all_profiles(self):
        """Get list of all profile names"""
        return list(self.users.keys())
    
    def delete_profile(self, name):
        """Delete a user profile"""
        if name in self.users:
            user = self.users[name]
            if user.data_file and os.path.exists(user.data_file):
                os.remove(user.data_file)
            del self.users[name]
            self.save_profiles_index()
            return True
        return False
    
    def save_profiles_index(self):
        """Save profiles index to file"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            profiles_list = list(self.users.keys())
            with open(self.profiles_file, 'w') as f:
                json.dump(profiles_list, f, indent=2)
        except Exception as e:
            print(f"Error saving profiles index: {e}")
    
    def load_all_profiles(self):
        """Load all user profiles from files"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            
            if os.path.exists(self.profiles_file):
                with open(self.profiles_file, 'r') as f:
                    profiles_list = json.load(f)
                
                for name in profiles_list:
                    user_file = os.path.join(self.data_dir, f"{name}.json")
                    if os.path.exists(user_file):
                        with open(user_file, 'r') as f:
                            user_data = json.load(f)
                        
                        user = User.from_dict(user_data)
                        user.data_file = user_file
                        self.users[name] = user
        except Exception as e:
            print(f"Error loading profiles: {e}")
    
    def get_global_statistics(self):
        """Get statistics across all users"""
        total_users = len(self.users)
        total_sleep_records = 0
        total_short_sleep = 0
        
        for user in self.users.values():
            stats = user.get_sleep_statistics()
            total_sleep_records += stats['total_records']
            total_short_sleep += stats['short_sleep_count']
        
        return {
            'total_users': total_users,
            'total_sleep_records': total_sleep_records,
            'total_short_sleep': total_short_sleep,
            'short_sleep_percentage': (total_short_sleep / total_sleep_records * 100) if total_sleep_records > 0 else 0
        }