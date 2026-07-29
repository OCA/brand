# © 2016 Therp BV <http://therp.nl>
# Copyright 2023 Onestein - Anjeel Haria
# © 2025 OBS Solutions BV <http://obs-solutions.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from base64 import b64decode
from io import BytesIO
from logging import getLogger

from odoo import fields, models

logger = getLogger(__name__)

try:
    # we need this to be sure PIL has loaded PDF support
    from PIL import PdfImagePlugin  # noqa: F401
except ImportError:
    logger.error("ImportError: The PdfImagePlugin could not be imported")

try:
    from PyPDF2 import PdfFileReader, PdfFileWriter  # pylint: disable=W0404
except ImportError:
    logger.debug("Can not import PyPDF2")


class Report(models.Model):
    _inherit = "ir.actions.report"

    use_brand_watermark = fields.Boolean(
        default=False,
        help="Use the pdf watermark defined globally in the brand settings.",
    )

    def _postprocess_wkhtmltopdf(self, result, **kwargs):
        docids = self.env.context.get("res_ids", False)
        report_sudo = self._get_report(kwargs.get("report_ref", False))
        if docids:
            kwargs.get("report_ref", False)
            model_name = self.model or report_sudo.model
            first_record_id = docids[0]
            record = self.env[model_name].browse(first_record_id)
            if (
                self.use_brand_watermark or report_sudo.use_brand_watermark
            ) and hasattr(record, "brand_id"):
                brand = record.brand_id
                if brand and brand.pdf_watermark:
                    watermark = b64decode(brand.pdf_watermark)

                    # Apply the watermark to the PDF
                    pdf = PdfFileWriter()
                    pdf_watermark = PdfFileReader(BytesIO(watermark))
                    for page in PdfFileReader(BytesIO(result)).pages:
                        watermark_page = pdf.addBlankPage(
                            page.mediaBox.getWidth(), page.mediaBox.getHeight()
                        )
                        watermark_page.mergePage(pdf_watermark.getPage(0))
                        watermark_page.mergePage(page)

                    pdf_content = BytesIO()
                    pdf.write(pdf_content)
                    result = pdf_content.getvalue()

        return result

    def _run_wkhtmltopdf(self, *args, **kwargs):
        result = super()._run_wkhtmltopdf(*args, **kwargs)
        return self._postprocess_wkhtmltopdf(result, **kwargs)
