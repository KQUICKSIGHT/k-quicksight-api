# from django.conf import settings
# import urllib.request as requests
# import json


# class Github:
#     """
#     Github class to fetch the user info and return it
#     """
#     @staticmethod
#     def validate(access_token):
#         """
#         validate method Queries the github url to fetch the user info
#         """
#         try:
#             headers = {
#                 "Authorization": f"token {access_token}",
#                 "content-type": "application/json",
#                 "Access-Control-Expose-Headers": "ETag, Link, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval"
#             }
#             user_info_url = "https://api.github.com/user/emails"
#             req = requests.Request(user_info_url, headers=headers)
#             response = requests.urlopen(req)
#             response = response.read()
#             data = response.decode('utf-8')
#             user_info = json.loads(data)
#             print(response)
#             return user_info[0]
#         except:
#             return "The token is either invalid or has expired"
import requests

class Github:
    """GitHub class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        Validate method queries the GitHub API to fetch the user info
        """
        try:
            headers = {'Authorization': f'token {auth_token}'}
            user_response = requests.get('https://api.github.com/user', headers=headers)
            user_response.raise_for_status()
            user_info = user_response.json()

            email_response = requests.get('https://api.github.com/user/emails', headers=headers)
            email_response.raise_for_status()
            emails = email_response.json()
            primary_email = next((email['email'] for email in emails if email['primary']), None)
            
            user_info['email'] = primary_email
            return user_info
        except Exception as e:
            return f"An error occurred: {str(e)}"

