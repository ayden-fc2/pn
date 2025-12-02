from flask import Blueprint, request, jsonify, session
from app.services.account_service import AccountService

bp = Blueprint('account', __name__, url_prefix='/account')

@bp.before_request
def check_auth():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

@bp.route('', methods=['GET', 'PUT'])
def account():
    user_id = session['user_id']

    if request.method == 'GET':
        details = AccountService.get_account_details(user_id)
        return jsonify(details)

    elif request.method == 'PUT':
        data = request.get_json()
        AccountService.update_account(user_id, data)
        return jsonify({'message': 'Account updated'})

@bp.route('/email', methods=['POST', 'DELETE'])
def manage_email():
    user_id = session['user_id']
    data = request.get_json()

    if request.method == 'POST':
        AccountService.add_email(user_id, data['email'])
        return jsonify({'message': 'Email added'})
    elif request.method == 'DELETE':
        AccountService.delete_email(user_id, data['email'])
        return jsonify({'message': 'Email deleted'})

@bp.route('/phone', methods=['POST', 'DELETE'])
def manage_phone():
    user_id = session['user_id']
    data = request.get_json()

    if request.method == 'POST':
        AccountService.add_phone(user_id, data['phone'])
        return jsonify({'message': 'Phone added'})
    elif request.method == 'DELETE':
        AccountService.delete_phone(user_id, data['phone'])
        return jsonify({'message': 'Phone deleted'})

@bp.route('/provider', methods=['POST', 'DELETE'])
def manage_provider():
    user_id = session['user_id']
    data = request.get_json()
    provider_id = data.get('provider_id')

    if request.method == 'POST':
        AccountService.add_provider(user_id, provider_id)
        return jsonify({'message': 'Provider linked'})
    elif request.method == 'DELETE':
        AccountService.delete_provider(user_id, provider_id)
        return jsonify({'message': 'Provider unlinked'})
