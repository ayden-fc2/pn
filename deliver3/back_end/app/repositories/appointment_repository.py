from app.db import query_db

class AppointmentRepository:
    @staticmethod
    def get_appointments_by_user(user_id):
        return query_db('''
            SELECT a.*, p.name as provider_name 
            FROM Appointments a 
            JOIN Providers p ON a.provider_id = p.provider_id 
            WHERE a.user_id = ?
        ''', [user_id])

    @staticmethod
    def create_appointment(user_id, provider_id, date, app_type):
        query_db('''
            INSERT INTO Appointments (user_id, provider_id, appointment_date, appointment_type)
            VALUES (?, ?, ?, ?)
        ''', [user_id, provider_id, date, app_type])

    @staticmethod
    def count_appointments_by_month(user_id, month):
        result = query_db('''
            SELECT count(*) as count FROM Appointments
            WHERE user_id = ? AND strftime('%Y-%m', appointment_date) = ?
        ''', [user_id, month], one=True)
        return result['count'] if result else 0

    @staticmethod
    def search_appointments(user_id, provider_name=None, app_type=None, start_date=None, end_date=None):
        query = '''
            SELECT a.*, p.name as provider_name 
            FROM Appointments a 
            JOIN Providers p ON a.provider_id = p.provider_id 
            WHERE a.user_id = ?
        '''
        params = [user_id]

        if provider_name:
            query += ' AND p.name LIKE ?'
            params.append(f'%{provider_name}%')
        if app_type:
            query += ' AND a.appointment_type LIKE ?'
            params.append(f'%{app_type}%')
        if start_date:
            query += ' AND a.appointment_date >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND a.appointment_date <= ?'
            params.append(end_date)

        return query_db(query, params)
