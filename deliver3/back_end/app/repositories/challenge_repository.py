from app.db import query_db

class ChallengeRepository:
    @staticmethod
    def get_all_challenges():
        return query_db('SELECT * FROM WellnessChallenges')

    @staticmethod
    def create_challenge(creator_id, name, description, start_date, end_date):
        query_db('''
            INSERT INTO WellnessChallenges (creator_id, name, description, start_date, end_date)
            VALUES (?, ?, ?, ?, ?)
        ''', [creator_id, name, description, start_date, end_date])

    @staticmethod
    def join_challenge(user_id, challenge_id):
        query_db('INSERT OR IGNORE INTO UserChallenges (user_id, challenge_id) VALUES (?, ?)', 
                 [user_id, challenge_id])

    @staticmethod
    def get_most_popular_challenge():
        return query_db('''
            SELECT c.name, count(uc.user_id) as participant_count
            FROM WellnessChallenges c
            JOIN UserChallenges uc ON c.challenge_id = uc.challenge_id
            GROUP BY c.challenge_id
            ORDER BY participant_count DESC
            LIMIT 1
        ''', one=True)
