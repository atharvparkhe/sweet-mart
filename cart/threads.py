import threading
from django.conf import settings
from django.core.mail import EmailMessage
from .utils import save_invoice

class generate_invoice(threading.Thread):
    def __init__(self, order):
        self.order = order
        threading.Thread.__init__(self)
    def run(self):
        try:
            sub = "Order summary"
            body = "Your order summary"
            msg = EmailMessage(sub, body, settings.EMAIL_HOST_USER, [self.order.owner.email])
            msg.content_subtype = "html"

            params = {
                "cart_obj" : self.order,
                "cart_items" : self.order.related_cart.all()
            }

            file_path, status = save_invoice(params)

            if status:
                msg.attach_file("data/invoice/" + file_path + ".pdf")
                print("Email send started")
                msg.send()
                print("Email send finished")
            else : pass
        except Exception as e:
            print(e)