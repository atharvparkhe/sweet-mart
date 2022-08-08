from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings


def save_invoice(params:dict):
    try:
        template = get_template("cart/invoice.html")
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        fname = str(uuid.uuid4())

        with open(str(settings.BASE_DIR) + f"/data/invoice/{fname}.pdf", "wb+") as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)

        if pdf.err:
            return "", False

        return fname, True

    except Exception as e:
        print(e)