from datetime import datetime
from app.repositories.metric_repository import MetricRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.challenge_repository import ChallengeRepository
from app.repositories.user_repository import UserRepository

class SummaryService:
    @staticmethod
    def get_monthly_summary(user_id, month):
        if not month:
            month = datetime.now().strftime('%Y-%m')

        stats = MetricRepository.get_monthly_stats(user_id, month)
        app_count = AppointmentRepository.count_appointments_by_month(user_id, month)

        return {
            'month': month,
            'metrics_stats': [dict(row) for row in stats],
            'appointment_count': app_count
        }

    @staticmethod
    def get_analytics():
        popular_challenge = ChallengeRepository.get_most_popular_challenge()
        active_user = UserRepository.get_most_active_user()

        return {
            'most_popular_challenge': dict(popular_challenge) if popular_challenge else None,
            'most_active_user': dict(active_user) if active_user else None
        }
