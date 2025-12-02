from app.db import query_db

class UserRepository:
    @staticmethod
    def get_user_by_id(user_id):
        return query_db('SELECT * FROM Users WHERE user_id = ?', [user_id], one=True)

    @staticmethod
    def get_user_by_credentials(user_id, password):
        return query_db('SELECT * FROM Users WHERE user_id = ? AND password = ?', [user_id, password], one=True)

    @staticmethod
    def update_user(user_id, first_name, last_name, address):
        query_db('UPDATE Users SET first_name = ?, last_name = ?, address = ? WHERE user_id = ?',
                 [first_name, last_name, address, user_id])

    @staticmethod
    def get_emails(user_id):
        return query_db('SELECT * FROM Emails WHERE user_id = ?', [user_id])

    @staticmethod
    def add_email(user_id, email):
        query_db('INSERT INTO Emails (user_id, email_address) VALUES (?, ?)', [user_id, email])

    @staticmethod
    def delete_email(user_id, email):
        query_db('DELETE FROM Emails WHERE user_id = ? AND email_address = ?', [user_id, email])

    @staticmethod
    def get_phones(user_id):
        return query_db('SELECT * FROM PhoneNumbers WHERE user_id = ?', [user_id])

    @staticmethod
    def add_phone(user_id, phone):
        query_db('INSERT INTO PhoneNumbers (user_id, phone_number) VALUES (?, ?)', [user_id, phone])

    @staticmethod
    def delete_phone(user_id, phone):
        query_db('DELETE FROM PhoneNumbers WHERE user_id = ? AND phone_number = ?', [user_id, phone])

    @staticmethod
    def get_providers(user_id):
        return query_db('''
            SELECT p.provider_id, p.name as provider_name, p.specialty 
            FROM Providers p
            JOIN UserProviders up ON p.provider_id = up.provider_id
            WHERE up.user_id = ?
        ''', [user_id])

    @staticmethod
    def get_all_providers():
        return query_db('SELECT provider_id, name as provider_name, specialty FROM Providers')

    @staticmethod
    def add_provider(user_id, provider_id):
        query_db('INSERT OR IGNORE INTO UserProviders (user_id, provider_id) VALUES (?, ?)', [user_id, provider_id])

    @staticmethod
    def delete_provider(user_id, provider_id):
        query_db('DELETE FROM UserProviders WHERE user_id = ? AND provider_id = ?', [user_id, provider_id])

    @staticmethod
    def get_most_active_user():
        return query_db('''
            SELECT u.first_name, u.last_name, count(hm.metric_id) as record_count
            FROM Users u
            JOIN HealthMetrics hm ON u.user_id = hm.user_id
            GROUP BY u.user_id
            ORDER BY record_count DESC
            LIMIT 1
        ''', one=True)
