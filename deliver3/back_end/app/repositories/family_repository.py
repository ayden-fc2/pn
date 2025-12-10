from app.db import query_db, get_db

class FamilyRepository:
    @staticmethod
    def get_user_family_group(user_id):
        return query_db('''
            SELECT fg.*, fm.role, fm.joined_at
            FROM FamilyGroup fg
            JOIN FamilyMembership fm ON fg.group_id = fm.group_id
            WHERE fm.user_id = ?
        ''', [user_id], one=True)

    @staticmethod
    def get_family_members(group_id):
        return query_db('''
            SELECT u.user_id, u.first_name, u.last_name, fm.role, fm.joined_at
            FROM Users u
            JOIN FamilyMembership fm ON u.user_id = fm.user_id
            WHERE fm.group_id = ?
        ''', [group_id])

    @staticmethod
    def create_family_group(name):
        db = get_db()
        cursor = db.execute('INSERT INTO FamilyGroup (name) VALUES (?)', [name])
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def delete_family_group(group_id):
        query_db('DELETE FROM FamilyGroup WHERE group_id = ?', [group_id])

    @staticmethod
    def add_member(group_id, user_id, role='Member'):
        query_db('INSERT INTO FamilyMembership (group_id, user_id, role) VALUES (?, ?, ?)', 
                 [group_id, user_id, role])

    @staticmethod
    def remove_member(group_id, user_id):
        query_db('DELETE FROM FamilyMembership WHERE group_id = ? AND user_id = ?', 
                 [group_id, user_id])
