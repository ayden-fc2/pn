from app.repositories.metric_repository import MetricRepository
from datetime import datetime

class MetricService:
    @staticmethod
    def add_metric(user_id, data):
        metric_type = data.get('type')
        value = data.get('value')
        date = data.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        if metric_type and value:
            MetricRepository.add_metric(user_id, metric_type, value, date)
