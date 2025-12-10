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
    def get_total_steps(user_id, month):
        result = query_db('''
            SELECT SUM(value) as total_steps
            FROM HealthMetrics
            WHERE user_id = ? AND metric_type = 'Steps' AND strftime('%Y-%m', recorded_date) = ?
        ''', [user_id, month], one=True)
        return result['total_steps'] if result and result['total_steps'] else 0

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
    def add_metric(user_id, metric_type, value, unit, date):
        query_db('''
            INSERT INTO HealthMetrics (user_id, metric_type, value, unit, recorded_date)
            VALUES (?, ?, ?, ?, ?)
        ''', [user_id, metric_type, value, unit, date])

    @staticmethod
    def get_recent_metrics(user_id, limit=50):
        return query_db('''
            SELECT * FROM HealthMetrics
            WHERE user_id = ?
            ORDER BY recorded_date DESC
            LIMIT ?
        ''', [user_id, limit])

    @staticmethod
    def delete_metric(user_id, metric_id):
        query_db('DELETE FROM HealthMetrics WHERE user_id = ? AND metric_id = ?', [user_id, metric_id])


