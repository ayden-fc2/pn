from app.repositories.metric_repository import MetricRepository
from datetime import datetime

class MetricService:
    @staticmethod
    def add_metric(user_id, data):
        metric_type = data.get('type')
        value = data.get('value')
        unit = data.get('unit')
        date = data.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        if metric_type and value:
            MetricRepository.add_metric(user_id, metric_type, value, unit, date)

    @staticmethod
    def get_history(user_id):
        metrics = MetricRepository.get_recent_metrics(user_id)
        return [dict(m) for m in metrics]

    @staticmethod
    def delete_metric(user_id, metric_id):
        MetricRepository.delete_metric(user_id, metric_id)
