from app.repositories.appointment_repository import AppointmentRepository
from datetime import datetime

class AppointmentService:
    @staticmethod
    def get_appointments(user_id):
        apps = AppointmentRepository.get_appointments_by_user(user_id)
        result = []
        for row in apps:
            row_dict = dict(row)
            # Handle date and time splitting
            dt_str = str(row_dict['appointment_date'])
            try:
                # Try parsing standard SQL datetime format
                if 'T' in dt_str:
                    dt = datetime.fromisoformat(dt_str)
                else:
                    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                
                row_dict['date'] = dt.strftime('%Y-%m-%d')
                row_dict['time'] = dt.strftime('%H:%M')
            except ValueError:
                # Fallback simple split
                parts = dt_str.split(' ')
                row_dict['date'] = parts[0]
                row_dict['time'] = parts[1] if len(parts) > 1 else ''
            
            # Map description
            row_dict['description'] = row_dict.get('appointment_type', '')
            result.append(row_dict)
        return result

    @staticmethod
    def book_appointment(user_id, data):
        date_str = data.get('date')
        time_str = data.get('time')
        # Ensure seconds are included
        if len(time_str) == 5:
            time_str += ':00'
        
        appointment_date = f"{date_str} {time_str}"
        app_type = data.get('description', 'General')
        memo = data.get('memo')
        
        AppointmentRepository.create_appointment(user_id, data['provider_id'], appointment_date, app_type, memo)

    @staticmethod
    def cancel_appointment(appointment_id, reason=None):
        AppointmentRepository.cancel_appointment(appointment_id, reason)

    @staticmethod
    def search_appointments(user_id, filters):
        results = AppointmentRepository.search_appointments(
            user_id,
            provider_name=filters.get('provider'),
            app_type=filters.get('type'),
            start_date=filters.get('start_date'),
            end_date=filters.get('end_date')
        )
        return [dict(row) for row in results]
