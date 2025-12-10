from app.repositories.user_repository import UserRepository

class AccountService:
    @staticmethod
    def get_account_details(user_id):
        user = UserRepository.get_user_by_id(user_id)
        emails = UserRepository.get_emails(user_id)
        phones = UserRepository.get_phones(user_id)
        providers = UserRepository.get_providers(user_id)
        
        # Convert rows to dicts and handle boolean fields
        provider_list = []
        for p in providers:
            d = dict(p)
            d['is_verified'] = bool(d.get('is_verified', 0))
            d['is_primary_care'] = bool(d.get('is_primary_care', 0))
            provider_list.append(d)

        email_list = []
        for e in emails:
            d = dict(e)
            d['is_verified'] = bool(d.get('is_verified', 0))
            email_list.append(d)

        phone_list = []
        for p in phones:
            d = dict(p)
            d['is_verified'] = bool(d.get('is_verified', 0))
            phone_list.append(d)

        return {
            'user': dict(user) if user else None,
            'emails': email_list,
            'phones': phone_list,
            'providers': provider_list
        }

    @staticmethod
    def get_all_providers():
        providers = UserRepository.get_all_providers()
        return [dict(p) for p in providers]

    @staticmethod
    def update_account(user_id, data):
        if 'first_name' in data and 'last_name' in data and 'address' in data:
            UserRepository.update_user(user_id, data['first_name'], data['last_name'], data['address'])

    @staticmethod
    def add_email(user_id, email):
        UserRepository.add_email(user_id, email)

    @staticmethod
    def delete_email(user_id, email):
        UserRepository.delete_email(user_id, email)

    @staticmethod
    def add_phone(user_id, phone):
        UserRepository.add_phone(user_id, phone)

    @staticmethod
    def delete_phone(user_id, phone):
        UserRepository.delete_phone(user_id, phone)

    @staticmethod
    def add_provider(user_id, provider_id):
        UserRepository.add_provider(user_id, provider_id)

    @staticmethod
    def delete_provider(user_id, provider_id):
        UserRepository.delete_provider(user_id, provider_id)

    @staticmethod
    def get_all_users():
        users = UserRepository.get_all_users()
        return [dict(u) for u in users]
