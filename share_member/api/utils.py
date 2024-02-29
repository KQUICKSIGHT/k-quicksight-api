
# base_url_analysis = "http://localhost:8000/api/v1/share-analysis/verify/"
# base_url_dataset = "http://localhost:8000/api/v1/share-dataset/verify/"
# base_url_dashboard = "http://localhost:8000/api/v1/share-dashboard/verify/"

base_url_analysis = "https://photostad-api.istad.co/api/v1/share-analysis/verify/"
base_url_dataset = "https://photostad-api.istad.co/api/v1/share-dataset/verify/"
base_url_dashboard = "https://photostad-api.istad.co/api/v1/share-dashboard/verify/"


def get_email_body_dataset(member_username, owner_name, owner_email, uuid, text="file"):

    return """
<html>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; text-align: center;">
    <div style="background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); margin: 0 auto; max-width: 600px;">
        <h1 style="color: #333;">Verification Email</h1>
        <p style="color: #777; font-size: 18px; margin: 20px 0;">Hi {member_name}, you have been added to a new {text}.</p>
        <p style="color: #777; font-size: 18px; margin: 20px 0;">From owner details below:</p>
        <p style="color: #777; font-size: 18px; margin: 20px 0;">Username: {owner_name}</p>
        <p style="color: #777; font-size: 18px; margin: 20px 0;">Email: {owner_email}</p>
        
        <div style="margin-top: 30px;">
            <a href="{base_url}{file_share_uuid}/accepted/" style="background-color: #4CAF50; color: #fff; padding: 10px 20px; text-align: center; text-decoration: none; margin-right: 10px; border-radius: 5px; display: inline-block;">Accept</a>
            <a href="{base_url}{file_share_uuid}/rejected/" style="background-color: #f44336; color: #fff; padding: 10px 20px; text-align: center; text-decoration: none; border-radius: 5px; display: inline-block;">Reject</a>
        </div>
    </div>
</body>
</html>

""".format(member_name=member_username, owner_email=owner_email, file_share_uuid=uuid, owner_name=owner_name, base_url=base_url_dataset, text=text)


def get_email_body_analysis(member_username, owner_name, owner_email, uuid, text="file"):

    return """
<html>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; text-align: center;">
    <div style="background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); margin: 0 auto; max-width: 600px;">
        <h1 style="color: #333;">Verification Email</h1>
        <p style="color: #777; font-size: 18px; margin: 20px 0;">Hi {member_name}, you have been added to a new {text}.</p>
        <p style="color: #777; font-size: 18px; margin: 20px 0;">From owner details below:</p>
        <p style="color: #777; font-size: 18px; margin: 20px 0;">Username: {owner_name}</p>
        <p style="color: #777; font-size: 18px; margin: 20px 0;">Email: {owner_email}</p>
        
        <div style="margin-top: 30px;">
            <a href="{base_url}{file_share_uuid}/accepted/" style="background-color: #4CAF50; color: #fff; padding: 10px 20px; text-align: center; text-decoration: none; margin-right: 10px; border-radius: 5px; display: inline-block;">Accept</a>
            <a href="{base_url}{file_share_uuid}/rejected/" style="background-color: #f44336; color: #fff; padding: 10px 20px; text-align: center; text-decoration: none; border-radius: 5px; display: inline-block;">Reject</a>
        </div>
    </div>
</body>
</html>
""".format(member_name=member_username, owner_email=owner_email, file_share_uuid=uuid, owner_name=owner_name, base_url=base_url_analysis, text=text)


def get_email_body_dashboard(member_username, owner_name, owner_email, uuid, text="file"):

    return """
<html>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; text-align: center;">
    <div style="background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); margin: 0 auto; max-width: 600px;">
        <h1 style="color: #333;">Verification Email</h1>
        <p style="color: #777; font-size: 18px; margin: 20px 0;">Hi {member_name}, you have been added to a new {text}.</p>
        <p style="color: #777; font-size: 18px; margin: 20px 0;">From owner details below:</p>
        <p style="color: #777; font-size: 18px; margin: 20px 0;">Username: {owner_name}</p>
        <p style="color: #777; font-size: 18px; margin: 20px 0;">Email: {owner_email}</p>
        
        <div style="margin-top: 30px;">
            <a href="{base_url}{file_share_uuid}/accepted/" style="background-color: #4CAF50; color: #fff; padding: 10px 20px; text-align: center; text-decoration: none; margin-right: 10px; border-radius: 5px; display: inline-block;">Accept</a>
            <a href="{base_url}{file_share_uuid}/rejected/" style="background-color: #f44336; color: #fff; padding: 10px 20px; text-align: center; text-decoration: none; border-radius: 5px; display: inline-block;">Reject</a>
        </div>
    </div>
</body>
</html>
""".format(member_name=member_username, owner_email=owner_email, file_share_uuid=uuid, owner_name=owner_name, base_url=base_url_dashboard, text=text)
