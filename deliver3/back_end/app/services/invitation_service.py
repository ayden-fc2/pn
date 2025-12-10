from app.repositories.invitation_repository import InvitationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.challenge_repository import ChallengeRepository

class InvitationService:
    @staticmethod
    def get_my_invitations(user_id):
        # Get user's emails
        emails = UserRepository.get_emails(user_id)
        all_invites = []
        for email_row in emails:
            email = email_row['email_address']
            invites = InvitationRepository.get_invitations_by_email(email)
            for inv in invites:
                all_invites.append(dict(inv))
        return all_invites

    @staticmethod
    def send_invitation(sender_id, data):
        InvitationRepository.create_invitation(
            sender_id, 
            data['type'], 
            data['target_email'], 
            data.get('challenge_id')
        )

    @staticmethod
    def respond_invitation(user_id, invitation_id, status):
        invitation = InvitationRepository.get_invitation_by_id(invitation_id)
        if not invitation:
            raise ValueError("Invitation not found")
        
        InvitationRepository.update_status(invitation_id, status)
        
        if status == 'Accepted':
            # Handle acceptance logic
            if invitation['type'] == 'Challenge' and invitation['challenge_id']:
                ChallengeRepository.join_challenge(user_id, invitation['challenge_id'])
            # Add other types logic here (e.g. Family)
