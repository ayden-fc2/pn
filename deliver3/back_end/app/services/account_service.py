from app.repositories.user_repository import UserRepository

class AccountService:
    @staticmethod
    def get_account_details(user_id):
        user = UserRepository.get_user_by_id(user_id)
        emails = UserRepository.get_emails(user_id)
        phones = UserRepository.get_phones(user_id)
        providers = UserRepository.get_providers(user_id)
        
        return {
            'user': dict(user) if user else None,
            'emails': [dict(e) for e in emails],
            'phones': [dict(p) for p in phones],
            'providers': [dict(p) for p in providers]
        }

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
