from flask import Blueprint, request, jsonify, session
from app.services.metric_service import MetricService

bp = Blueprint('metrics', __name__, url_prefix='/metrics')

@bp.before_request
def check_auth():
    if request.method == 'OPTIONS':
        return
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

@bp.route('', methods=['POST'])
def add_metric():
    user_id = session['user_id']
    data = request.get_json()
    MetricService.add_metric(user_id, data)
    return jsonify({'message': 'Metric added'})
