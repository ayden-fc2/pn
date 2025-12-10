from flask import Blueprint, request, jsonify, session
from app.services.family_service import FamilyService

bp = Blueprint('family', __name__, url_prefix='/family')

@bp.before_request
def check_auth():
    if request.method == 'OPTIONS':
        return
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

@bp.route('', methods=['GET', 'POST'])
def family():
    user_id = session['user_id']

    if request.method == 'GET':
        info = FamilyService.get_family_info(user_id)
        return jsonify(info if info else {})

    elif request.method == 'POST':
        data = request.get_json()
        try:
            FamilyService.create_family(user_id, data['name'])
            return jsonify({'message': 'Family group created'})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

@bp.route('/leave', methods=['POST'])
def leave_family():
    user_id = session['user_id']
    FamilyService.leave_family(user_id)
    return jsonify({'message': 'Left family group'})
