from app.db import query_db

class DelegationRepository:
    @staticmethod
    def get_dependents(guardian_id):
        return query_db('''
            SELECT u.user_id, u.first_name, u.last_name, ud.created_at
            FROM Users u
            JOIN UserDelegation ud ON u.user_id = ud.dependent_id
            WHERE ud.guardian_id = ?
        ''', [guardian_id])

    @staticmethod
    def get_guardians(dependent_id):
        return query_db('''
            SELECT u.user_id, u.first_name, u.last_name, ud.created_at
            FROM Users u
            JOIN UserDelegation ud ON u.user_id = ud.guardian_id
            WHERE ud.dependent_id = ?
        ''', [dependent_id])

    @staticmethod
    def create_delegation(guardian_id, dependent_id):
        query_db('INSERT INTO UserDelegation (guardian_id, dependent_id) VALUES (?, ?)', 
                 [guardian_id, dependent_id])

    @staticmethod
    def remove_delegation(guardian_id, dependent_id):
        query_db('DELETE FROM UserDelegation WHERE guardian_id = ? AND dependent_id = ?', 
                 [guardian_id, dependent_id])
