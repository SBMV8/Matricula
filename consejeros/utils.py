from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse

def render_to_pdf(template_src, context_dict):
    # Obtener el template HTML
    template = get_template(template_src)
    html = template.render(context_dict)

    # Crear un buffer en memoria
    result = BytesIO()

    # Usar xhtml2pdf para generar el PDF a partir del HTML
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    # Verificar si se generó correctamente
    if pdf.err:
        return None
    return result.getvalue()