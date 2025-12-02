from flask import Blueprint, request, jsonify, session
from app.services.auth_service import AuthService

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')
    
    user = AuthService.login(user_id, password)
    
    if user:
        session['user_id'] = user['user_id']
        return jsonify({'message': 'Logged in successfully', 'user': user})
    return jsonify({'error': 'Invalid credentials'}), 401

@bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'})
