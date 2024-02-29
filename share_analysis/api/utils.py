
base_url = "http://localhost:8000/api/v1/share-member-dataset/verify/"

base_url = "https://photostad-api.istad.co/api/v1/share-dataset/verify/"


def get_email_body(member_username, owner_name, owner_email, uuid):

    return """
<html>
    <body>
        <p>Hi {member_name}, you have been added to a new file.</p><br /><br />
        <p>From owner detail below: </p>
        <p>username:  {owner_name}</p>
        <p>email:  {owner_email}</p>

        <p>
        
            <a href="{base_url}{file_share_uuid}/accepted/" style="background-color: green; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; margin-right: 10px;">
                Accept
            </a>
            <a href="{base_url}{file_share_uuid}/rejected/" style="background-color: red; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block;">
                Reject
            </a>
        </p>
    </body>
</html>
""".format(member_name=member_username, owner_email=owner_email, file_share_uuid=uuid, owner_name=owner_name, base_url=base_url)
