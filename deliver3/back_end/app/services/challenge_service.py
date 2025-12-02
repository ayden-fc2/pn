from app.repositories.challenge_repository import ChallengeRepository

class ChallengeService:
    @staticmethod
    def get_all_challenges(user_id=None):
        if user_id:
            challenges = ChallengeRepository.get_challenges_with_status(user_id)
        else:
            challenges = ChallengeRepository.get_all_challenges()
            
        result = []
        for row in challenges:
            r = dict(row)
            r['title'] = r['name'] # Map name to title for frontend
            r['joined'] = bool(r.get('joined', 0))
            result.append(r)
        return result

    @staticmethod
    def create_challenge(user_id, data):
        ChallengeRepository.create_challenge(
            user_id, 
            data['name'], 
            data['description'], 
            data['start_date'], 
            data['end_date']
        )

    @staticmethod
    def join_challenge(user_id, challenge_id):
        ChallengeRepository.join_challenge(user_id, challenge_id)

    @staticmethod
    def leave_challenge(user_id, challenge_id):
        ChallengeRepository.leave_challenge(user_id, challenge_id)

