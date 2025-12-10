from app.db import query_db

class ChallengeRepository:
    @staticmethod
    def get_all_challenges():
        return query_db('SELECT * FROM WellnessChallenges')

    @staticmethod
    def get_challenges_with_status(user_id):
        return query_db('''
            SELECT c.*, 
                   CASE WHEN uc.user_id IS NOT NULL THEN 1 ELSE 0 END as joined,
                   uc.status as user_status,
                   uc.progress_value
            FROM WellnessChallenges c
            LEFT JOIN UserChallenges uc ON c.challenge_id = uc.challenge_id AND uc.user_id = ?
        ''', [user_id])

    @staticmethod
    def create_challenge(creator_id, name, description, goal, start_date, end_date):
        query_db('''
            INSERT INTO WellnessChallenges (creator_id, name, description, goal, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', [creator_id, name, description, goal, start_date, end_date])

    @staticmethod
    def update_progress(user_id, challenge_id, progress_value):
        query_db('''
            UPDATE UserChallenges 
            SET progress_value = ? 
            WHERE user_id = ? AND challenge_id = ?
        ''', [progress_value, user_id, challenge_id])

    @staticmethod
    def join_challenge(user_id, challenge_id):
        query_db('INSERT OR IGNORE INTO UserChallenges (user_id, challenge_id) VALUES (?, ?)', 
                 [user_id, challenge_id])

    @staticmethod
    def leave_challenge(user_id, challenge_id):
        query_db('DELETE FROM UserChallenges WHERE user_id = ? AND challenge_id = ?', 
                 [user_id, challenge_id])

    @staticmethod
    def count_active_challenges(user_id):
        result = query_db('''
            SELECT count(*) as count 
            FROM UserChallenges uc
            JOIN WellnessChallenges c ON uc.challenge_id = c.challenge_id
            WHERE uc.user_id = ? AND c.end_date >= date('now')
        ''', [user_id], one=True)
        return result['count'] if result else 0

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

    @staticmethod
    def get_active_challenges(user_id):
        return query_db('''
            SELECT c.*, uc.progress_value, uc.status as user_status
            FROM WellnessChallenges c
            JOIN UserChallenges uc ON c.challenge_id = uc.challenge_id
            WHERE uc.user_id = ? AND uc.status = 'Active' AND c.end_date >= date('now')
        ''', [user_id])
