from flask import Blueprint, request, jsonify, session
from app.services.report_service import ReportService

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.before_request
def check_auth():
    if request.method == 'OPTIONS':
        return
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

@bp.route('', methods=['GET'])
def get_reports():
    user_id = session['user_id']
    reports = ReportService.get_user_reports(user_id)
    return jsonify(reports)
