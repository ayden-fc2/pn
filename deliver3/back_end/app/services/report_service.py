from app.repositories.report_repository import ReportRepository

class ReportService:
    @staticmethod
    def get_user_reports(user_id):
        reports = ReportRepository.get_reports(user_id)
        return [dict(r) for r in reports]

    @staticmethod
    def generate_report(user_id, month):
        # In a real app, this would calculate stats from other tables
        # For now, we'll just create a dummy report
        summary = f"Health summary for {month}"
        steps_total = 0 # Placeholder
        ReportRepository.create_report(user_id, month, summary, steps_total)
