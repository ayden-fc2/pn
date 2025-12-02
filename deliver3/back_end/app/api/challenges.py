from flask import Blueprint, request, jsonify, session
from app.services.challenge_service import ChallengeService

bp = Blueprint('challenges', __name__, url_prefix='/challenges')

@bp.before_request
def check_auth():
    if request.method == 'OPTIONS':
        return
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

@bp.route('', methods=['GET', 'POST'])
def challenges():
    user_id = session['user_id']

    if request.method == 'GET':
        challenges = ChallengeService.get_all_challenges(user_id)
        return jsonify(challenges)

    elif request.method == 'POST':
        data = request.get_json()
        ChallengeService.create_challenge(user_id, data)
        return jsonify({'message': 'Challenge created'})

@bp.route('/<int:challenge_id>/join', methods=['POST'])
def join_challenge(challenge_id):
    user_id = session['user_id']
    ChallengeService.join_challenge(user_id, challenge_id)
    return jsonify({'message': 'Joined challenge'})

@bp.route('/<int:challenge_id>/leave', methods=['POST'])
def leave_challenge(challenge_id):
    user_id = session['user_id']
    ChallengeService.leave_challenge(user_id, challenge_id)
    return jsonify({'message': 'Left challenge'})

