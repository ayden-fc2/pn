from flask import Blueprint, request, jsonify, session
from app.services.summary_service import SummaryService

bp = Blueprint('summary', __name__)

@bp.before_request
def check_auth():
    if request.method == 'OPTIONS':
        return
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

@bp.route('/summary', methods=['GET'])
def dashboard_summary():
    user_id = session['user_id']
    summary = SummaryService.get_dashboard_summary(user_id)
    return jsonify(summary)

@bp.route('/summary/monthly', methods=['GET'])
def monthly_summary():
    user_id = session['user_id']
    month = request.args.get('month')
    
    summary = SummaryService.get_monthly_summary(user_id, month)
    return jsonify(summary)

@bp.route('/analytics', methods=['GET'])
def analytics():
    # Analytics might be public or admin only, but let's keep it open or check auth if needed
    # For now, let's assume it's accessible
    data = SummaryService.get_analytics()
    return jsonify(data)
