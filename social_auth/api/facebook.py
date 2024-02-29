
import facebook


class Facebook:


    @staticmethod
    def validate(auth_token):

        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            fields = 'id,name,email,picture,birthday,gender,hometown'
            profile = graph.request(f'/me?fields={fields}')
            print(profile)
            return profile
        except:
            return "The token is invalid or expired."