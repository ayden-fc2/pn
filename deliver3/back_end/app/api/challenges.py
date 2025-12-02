from flask import Blueprint, request, jsonify, session
from app.services.challenge_service import ChallengeService

bp = Blueprint('challenges', __name__, url_prefix='/challenges')

@bp.before_request
def check_auth():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

@bp.route('', methods=['GET', 'POST'])
def challenges():
    user_id = session['user_id']

    if request.method == 'GET':
        challenges = ChallengeService.get_all_challenges()
        return jsonify(challenges)

    elif request.method == 'POST':
        data = request.get_json()
        ChallengeService.create_challenge(user_id, data)
        return jsonify({'message': 'Challenge created'})

@bp.route('/join', methods=['POST'])
def join_challenge():
    user_id = session['user_id']
    data = request.get_json()
    ChallengeService.join_challenge(user_id, data['challenge_id'])
    return jsonify({'message': 'Joined challenge'})
