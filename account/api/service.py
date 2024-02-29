from user.models import User

class AccountService:

    @staticmethod
    def find_email_and_verified(email):
        try:
            user = User.objects.get(email=email, is_verified=True)
            return True  # Email found and user is verified
        except User.DoesNotExist:
            return False  # Email not found or
