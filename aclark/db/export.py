from django.http import HttpResponse
from django_xhtml2pdf.utils import generate_pdf
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx import Document
from docx.shared import Inches
from io import StringIO
from lxml import etree

docx = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def render_doc(context, **kwargs):
    """
    """
    # https://python-docx.readthedocs.io/en/latest/#what-it-can-do
    document = Document()
    filename = kwargs.get("filename")
    item = context["item"]
    document.add_heading(item.title, 0)
    p = document.add_paragraph(item.note)
    response = HttpResponse(content_type=docx)
    response["Content-Disposition"] = "attachment; filename=%s" % filename
    document.save(response)
    return response


def render_pdf(context, **kwargs):
    """
    """
    filename = kwargs.get("filename")
    template = kwargs.get("template")
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "filename=%s" % filename
    return generate_pdf(template, context=context, file_object=response)
