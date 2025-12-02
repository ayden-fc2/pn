from app.repositories.user_repository import UserRepository

class AuthService:
    @staticmethod
    def login(user_id, password):
        user = UserRepository.get_user_by_credentials(user_id, password)
        if user:
            return dict(user)
        return None
