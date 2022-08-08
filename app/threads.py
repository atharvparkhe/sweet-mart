import threading
from django.conf import settings
from django.core.mail import send_mail

class send_contact_email(threading.Thread):
    def __init__(self, email, name):
        self.email = email
        self.name = name
        threading.Thread.__init__(self)
    def run(self):
        try:
            subject = "Link to verify the your Account"
            message = f"Hay {self.name} !\nThanks for filling up the Contact Form.\nWe will reachout to you as soon as possible."
            email_from = settings.EMAIL_HOST_USER
            print("Email send started")
            send_mail(subject , message ,email_from ,[self.email])
            print("Email send finished")
        except Exception as e:
            print(e)