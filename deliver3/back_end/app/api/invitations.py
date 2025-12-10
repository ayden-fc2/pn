from flask import Blueprint, request, jsonify, session
from app.services.invitation_service import InvitationService

bp = Blueprint('invitations', __name__, url_prefix='/invitations')

@bp.before_request
def check_auth():
    if request.method == 'OPTIONS':
        return
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

@bp.route('', methods=['GET', 'POST'])
def invitations():
    user_id = session['user_id']

    if request.method == 'GET':
        invites = InvitationService.get_my_invitations(user_id)
        return jsonify(invites)

    elif request.method == 'POST':
        data = request.get_json()
        InvitationService.send_invitation(user_id, data)
        return jsonify({'message': 'Invitation sent'})

@bp.route('/<int:invitation_id>/respond', methods=['POST'])
def respond(invitation_id):
    user_id = session['user_id']
    data = request.get_json()
    status = data.get('status') # Accepted / Rejected
    try:
        InvitationService.respond_invitation(user_id, invitation_id, status)
        return jsonify({'message': f'Invitation {status}'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
