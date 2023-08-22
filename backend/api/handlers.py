import io
from config.settings import STATIC_ROOT
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def create_and_download_pdf_file(ingredients):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    x, y = 50, 770
    pdfmetrics.registerFont(
            TTFont('Roboto Bold', STATIC_ROOT + '/fonts/Roboto-Bold.ttf')
        )
    pdfmetrics.registerFont(
            TTFont('Roboto', STATIC_ROOT + '/fonts/Roboto-Regular.ttf')
        )
    pdf.setFont("Roboto Bold", 24)
    pdf.drawString(x, y, 'Список покупок')
    pdf.setFont("Roboto", 15)
    y -= 20
    for index, ingredient in enumerate(ingredients, start=1):
        name, unit, amount = ingredient
        y -= 20
        pdf.drawString(x, y, f'{index}. {name} {amount} {unit}')

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return FileResponse(buffer,
                        as_attachment=True,
                        filename="download_shopping_cart.pdf")
