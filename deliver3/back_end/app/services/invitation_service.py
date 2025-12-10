from app.repositories.invitation_repository import InvitationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.challenge_repository import ChallengeRepository
from app.repositories.family_repository import FamilyRepository
from datetime import datetime, timedelta

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
        
        # Check expiry (15 days)
        created_at_str = str(invitation['created_at'])
        if 'T' in created_at_str:
            created_at = datetime.fromisoformat(created_at_str)
        else:
            created_at = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S')
            
        if datetime.now() > created_at + timedelta(days=15):
            InvitationRepository.update_status(invitation_id, 'Expired')
            raise ValueError("Invitation has expired")
        
        InvitationRepository.update_status(invitation_id, status)
        
        if status == 'Accepted':
            # Handle acceptance logic
            if invitation['type'] == 'Challenge' and invitation['challenge_id']:
                ChallengeRepository.join_challenge(user_id, invitation['challenge_id'])
            elif invitation['type'] == 'Family':
                # Check if user is already in a family
                if FamilyRepository.get_user_family_group(user_id):
                    raise ValueError("You are already in a family group. Please leave your current group before joining a new one.")

                # Add user to sender's family group
                sender_group = FamilyRepository.get_user_family_group(invitation['sender_id'])
                if sender_group:
                    FamilyRepository.add_member(sender_group['group_id'], user_id)
                else:
                    # If sender has no group (shouldn't happen if logic is correct), maybe create one?
                    # For now, we assume sender must be in a group to send family invite.
                    pass
