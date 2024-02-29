
from django.contrib.auth import authenticate
from user.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from role.models import Role
from user_role.models import UserRole


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id=None, email=None, name=None, fullname=None, avatar=None):

    filtered_user_by_email = User.objects.filter(email=email)
    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=os.environ.get('GOOGLE_CLIENT_ID')
            )
            
            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'data': registered_user.tokens()
            }

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' +
                filtered_user_by_email[0].auth_provider
            )

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': os.environ.get('GOOGLE_CLIENT_ID')
        }

        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.full_name = fullname
        user.avatar = avatar
        user.save()
        role_instance = Role.objects.get(id=2)
        user_role = UserRole()
        user_role.user = user  # Assuming 'user' is an instance of the User model
        # Assuming 'role_instance' is an instance of the Role model
        user_role.role = role_instance
        user_role.save()
        new_user = authenticate(
            email=email, password=os.environ.get('GOOGLE_CLIENT_ID'))
        print("work chento")
        return {
            'email': new_user.email,
            'username': new_user.username,
            'data': new_user.tokens()
        }
