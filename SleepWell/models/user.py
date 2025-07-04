
class User:
    def __init__(self, name, ideal_sleep_hour=22):
        self.name = name
        self.ideal_sleep_hour = ideal_sleep_hour

    def set_sleep_goal(self, hour):
        self.ideal_sleep_hour = hour
