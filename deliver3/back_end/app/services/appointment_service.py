from app.repositories.appointment_repository import AppointmentRepository

class AppointmentService:
    @staticmethod
    def get_appointments(user_id):
        apps = AppointmentRepository.get_appointments_by_user(user_id)
        return [dict(row) for row in apps]

    @staticmethod
    def book_appointment(user_id, data):
        AppointmentRepository.create_appointment(user_id, data['provider_id'], data['date'], data['type'])

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
