from app.repositories.report_repository import ReportRepository
from app.repositories.metric_repository import MetricRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.challenge_repository import ChallengeRepository

class ReportService:
    @staticmethod
    def get_user_reports(user_id):
        reports = ReportRepository.get_reports(user_id)
        return [dict(r) for r in reports]

    @staticmethod
    def generate_report(user_id, month):
        # Calculate stats from HealthMetrics
        stats = MetricRepository.get_monthly_stats(user_id, month)
        
        # Calculate total steps
        steps_total = 0
        weight_avg = 0
        
        summary_parts = []
        
        for stat in stats:
            m_type = stat['metric_type']
            avg_val = stat['avg_val']
            if m_type == 'Steps':
                # For steps, we might want SUM instead of AVG, but get_monthly_stats does AVG/MIN/MAX.
                # Let's assume we want to sum them up. We need a new repository method for SUM or just use AVG * days?
                # Let's just use the AVG for now as a proxy or fetch sum specifically.
                # Actually, let's fetch SUM for steps specifically.
                pass
            elif m_type == 'Weight':
                weight_avg = avg_val
                summary_parts.append(f"Avg Weight: {avg_val:.1f}kg")
            elif m_type == 'Blood Pressure':
                summary_parts.append(f"Avg BP: {avg_val:.0f} mmHg")

        # Get total steps specifically
        total_steps_res = MetricRepository.get_total_steps(user_id, month)
        if total_steps_res:
            steps_total = total_steps_res
            summary_parts.append(f"Total Steps: {steps_total}")

        # Count appointments
        app_count = AppointmentRepository.count_appointments_by_month(user_id, month)
        if app_count > 0:
            summary_parts.append(f"Appointments: {app_count}")

        summary = ". ".join(summary_parts) + "."
        if not summary_parts:
            summary = "No activity recorded for this month."

        ReportRepository.create_report(user_id, month, summary, steps_total)

