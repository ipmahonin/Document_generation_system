from weasyprint import HTML
from jinja2 import Template
import os

def render_pdf_from_html(
        template_text: str,
        data: dict,
        output_pdf_path: str
):
    template = Template(template_text)

    html_content = template.render(data)

    HTML(string=html_content).write_pdf(output_pdf_path)

    return output_pdf_path


def get_output_pdf_path(request_id: str, output_dir: str = 'pdf_data'):
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, f'{request_id}.pdf')

