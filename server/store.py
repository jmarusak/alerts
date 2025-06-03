import json
from typing import List

from alert import Alert

class Store:
    def __init__(self):
        self.alerts: List[Alert] = []

    def add_or_update(self, new_alert: Alert) -> str:
        for idx, alert in enumerate(self.alerts):
            if alert.symbol == new_alert.symbol:
                self.alerts[idx] = new_alert
                return 'updated'
        self.alerts.append(new_alert)
        return 'added'

    def delete(self, symbol: str) -> bool:
        initial_count = len(self.alerts)
        self.alerts = [alert for alert in self.alerts if alert.symbol != symbol]
        return len(self.alerts) < initial_count

    def get_all(self) -> List[Alert]:
        return self.alerts

    def export(self) -> None:
        with open('data/alerts.json', 'w') as f:
            json.dump([alert for alert in self.alerts], f, indent=2)
