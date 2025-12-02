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

    @staticmethod
    def get_latest_metric(user_id, metric_type):
        result = query_db('''
            SELECT value FROM HealthMetrics
            WHERE user_id = ? AND metric_type = ?
            ORDER BY recorded_date DESC
            LIMIT 1
        ''', [user_id, metric_type], one=True)
        return result['value'] if result else None

    @staticmethod
    def add_metric(user_id, metric_type, value, date):
        query_db('''
            INSERT INTO HealthMetrics (user_id, metric_type, value, recorded_date)
            VALUES (?, ?, ?, ?)
        ''', [user_id, metric_type, value, date])


