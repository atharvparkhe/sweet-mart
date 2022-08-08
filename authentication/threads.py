from threading import Thread
from django.conf import settings
from django.core.mail import send_mail


class send_verification_email(Thread):
    def __init__(self, email, tok):
        self.email = email
        self.tok = tok
        Thread.__init__(self)
    def run(self):
        try:
            otp = settings.BASE_URL + "verify/" + self.tok + "/"
            subject = "Link to verify the your Account"
            message = f"Click the link to verify your account\n {otp}"
            email_from = settings.EMAIL_HOST_USER
            print("Email send started")
            send_mail(subject , message ,email_from ,[self.email])
            print("Email send finished")
        except Exception as e:
            print(e)

class send_forgot_link(Thread):
    def __init__(self, email, tok):
        self.email = email
        self.tok = tok
        Thread.__init__(self)
    def run(self):
        try:
            otp = settings.BASE_URL + "reset/" + self.tok + "/"
            subject = "Link to change password"
            message = f"Click the link to reset your account password\n {otp}"
            email_from = settings.EMAIL_HOST_USER
            print("Email send started")
            send_mail(subject , message ,email_from ,[self.email])
            print("Email send finished")
        except Exception as e:
                print(e)