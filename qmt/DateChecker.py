import datetime
import threading
from XiaoHei import xiaohei


class DateChecker:
    def __init__(self):
        self.events = []
        self.weekday_map = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6
        }

    def add_event(self, month=None, day=None, weekday=None, hour=None, minute=None, event_name=None):
        self.events.append({
            'month': month,
            'day': day,
            'weekday': weekday,
            'hour': hour,
            'minute': minute,
            'event_name': event_name,
            'last_reminded': None  # Add a field to track the last reminded date
        })

    def check_events(self):
        now = datetime.datetime.now()
        for event in self.events:
            if event['month'] is None or now.month == event['month']:
                if event['day'] is None or now.day == event['day']:
                    if event['weekday'] is None or now.weekday() == self.weekday_map[event['weekday']]:
                        if event['hour'] is None or now.hour == event['hour']:
                            if event['minute'] is None or now.minute == event['minute']:
                                # Check if the event has been reminded today
                                if event['last_reminded'] is None or event['last_reminded'].date() != now.date():
                                    xiaohei.send_text(f"Reminder: {event['event_name']}")
                                    event['last_reminded'] = now  # Update the last reminded date

    def start(self):
        self.check_events()
        # 60s-后执行
        threading.Timer(60, self.start).start()  # Check every minute


date_checker = DateChecker()


def registChecker():
    date_checker.add_event(day=29, event_name="统计当前自己资金")  # Add monthly tasks
    date_checker.start()  # Start the checker
