from app.db import query_db

class MetricRepository:
    @staticmethod
    def get_monthly_stats(user_id, month):
        return query_db('''
            SELECT metric_type, AVG(value) as avg_val, MIN(value) as min_val, MAX(value) as max_val
            FROM HealthMetrics
            WHERE user_id = ? AND strftime('%Y-%m', recorded_date) = ?
            GROUP BY metric_type
        ''', [user_id, month])
