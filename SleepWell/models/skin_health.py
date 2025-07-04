
import json
from datetime import datetime
from models.tracker import Tracker

class SkinHealth(Tracker):
    def __init__(self, filename="data/skin_data.json"):
        self.filename = filename

    def log_entry(self, data):
        data['timestamp'] = datetime.now().isoformat()
        all_data = self._load_data()
        all_data.append(data)
        self._save_data(all_data)

    def view_entries(self):
        return self._load_data()

    def _load_data(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except:
            return []

    def _save_data(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)
