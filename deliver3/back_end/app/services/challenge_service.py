from app.repositories.challenge_repository import ChallengeRepository

class ChallengeService:
    @staticmethod
    def get_all_challenges():
        challenges = ChallengeRepository.get_all_challenges()
        return [dict(row) for row in challenges]

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
