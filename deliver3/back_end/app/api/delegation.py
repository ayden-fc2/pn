from flask import Blueprint, request, jsonify, session
from app.services.delegation_service import DelegationService

bp = Blueprint('delegation', __name__, url_prefix='/delegation')

@bp.before_request
def check_auth():
    if request.method == 'OPTIONS':
        return
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

@bp.route('', methods=['GET'])
def get_delegations():
    user_id = session['user_id']
    data = DelegationService.get_delegations(user_id)
    return jsonify(data)

@bp.route('/add', methods=['POST'])
def add_dependent():
    user_id = session['user_id']
    data = request.get_json()
    try:
        DelegationService.add_dependent(user_id, data['dependent_id'])
        return jsonify({'message': 'Dependent added'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/remove', methods=['POST'])
def remove_delegation():
    user_id = session['user_id']
    data = request.get_json()
    # If removing a dependent (I am guardian)
    if 'dependent_id' in data:
        DelegationService.remove_delegation(user_id, data['dependent_id'])
    # If removing a guardian (I am dependent)
    elif 'guardian_id' in data:
        DelegationService.remove_delegation(data['guardian_id'], user_id)
    
    return jsonify({'message': 'Delegation removed'})
