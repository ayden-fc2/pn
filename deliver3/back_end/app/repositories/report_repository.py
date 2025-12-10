from app.db import query_db

class ReportRepository:
    @staticmethod
    def get_reports(user_id):
        return query_db('SELECT * FROM MonthlyReport WHERE user_id = ? ORDER BY month DESC', [user_id])

    @staticmethod
    def create_report(user_id, month, summary, steps_total):
        query_db('''
            INSERT INTO MonthlyReport (user_id, month, summary, steps_total)
            VALUES (?, ?, ?, ?)
        ''', [user_id, month, summary, steps_total])
