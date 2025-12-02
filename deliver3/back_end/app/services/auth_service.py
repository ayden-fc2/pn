from app.repositories.user_repository import UserRepository

class AuthService:
    @staticmethod
    def login(email, password):
        user = UserRepository.get_user_by_credentials(email, password)
        if user:
            return dict(user)
        return None
