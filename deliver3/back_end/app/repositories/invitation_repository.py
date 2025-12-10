from app.db import query_db

class InvitationRepository:
    @staticmethod
    def get_invitations_by_email(email):
        return query_db('''
            SELECT i.*, u.first_name as sender_name, u.last_name as sender_last_name,
                   wc.name as challenge_name
            FROM Invitation i
            JOIN Users u ON i.sender_id = u.user_id
            LEFT JOIN WellnessChallenges wc ON i.challenge_id = wc.challenge_id
            WHERE i.target_email = ?
            ORDER BY 
                CASE WHEN i.status = 'Pending' THEN 0 ELSE 1 END,
                i.created_at DESC
        ''', [email])

    @staticmethod
    def create_invitation(sender_id, type, target_email, challenge_id=None):
        query_db('''
            INSERT INTO Invitation (sender_id, type, target_email, challenge_id)
            VALUES (?, ?, ?, ?)
        ''', [sender_id, type, target_email, challenge_id])

    @staticmethod
    def update_status(invitation_id, status):
        query_db('UPDATE Invitation SET status = ? WHERE invitation_id = ?', 
                 [status, invitation_id])

    @staticmethod
    def get_invitation_by_id(invitation_id):
        return query_db('SELECT * FROM Invitation WHERE invitation_id = ?', [invitation_id], one=True)

    @staticmethod
    def count_pending_invitations(email):
        result = query_db('''
            SELECT count(*) as count 
            FROM Invitation 
            WHERE target_email = ? AND status = 'Pending'
        ''', [email], one=True)
        return result['count'] if result else 0
