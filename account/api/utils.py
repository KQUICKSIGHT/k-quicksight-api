from django.core.mail import EmailMessage


import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']],
        )
        email.content_subtype = 'html'
        EmailThread(email).start()

    def get_html_verify(code):
        return """
        <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Verification Code</title>
    <link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet'>
    <style>
        .email-template {
            width: 100%;
            max-width: 600px;
            margin: 20px auto;
            font-family: 'Open Sans', sans-serif;
            background-color: #f5f5f5;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .email-header {
            background-color: #0346A5;
            color: #ffffff;
            text-align: center;
            padding: 20px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }

        .email-content {
            padding: 20px;
            text-align: center;
        }

        .verification-code {
            font-size: 36px;
            padding: 15px;
            background-color: #0346A5;
            color: #ffffff;
            border-radius: 5px;
            display: inline-block;
        }

        .email-footer {
            text-align: center;
            padding: 20px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        }
    </style>
</head>

<body>
    <div class="email-template">
        <div class="email-header">
            <h1>Email Verification Code</h1>
        </div>
        <div class="email-content">
            <p>Please use the following verification code:</p>
            <div class="verification-code">"""+str(code)+"""</div>
            <p>This code is valid for 30 minutes.</p>
        </div>
        <div class="email-footer">
            <p>Thank you for using our services!</p>
        </div>
    </div>
</body>

</html>


        """
