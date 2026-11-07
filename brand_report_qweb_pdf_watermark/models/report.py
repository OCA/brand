# © 2016 Therp BV <http://therp.nl>
# Copyright 2023 Onestein - Anjeel Haria
# © 2025 OBS Solutions BV <http://obs-solutions.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from base64 import b64decode
from io import BytesIO
from logging import getLogger

from PIL import Image

from odoo import api, fields, models
from odoo.tools.pdf import PdfFileReader, PdfFileWriter, PdfReadError

logger = getLogger(__name__)


class Report(models.Model):
    _inherit = "ir.actions.report"

    use_brand_watermark = fields.Boolean(
        default=False,
        help="Use the pdf watermark defined on the brand of the printed record.",
    )

    @api.model
    def _run_wkhtmltopdf(
        self,
        bodies,
        report_ref=False,
        header=None,
        footer=None,
        landscape=False,
        specific_paperformat_args=None,
        set_viewport_size=False,
    ):
        result = super()._run_wkhtmltopdf(
            bodies,
            report_ref=report_ref,
            header=header,
            footer=footer,
            landscape=landscape,
            specific_paperformat_args=specific_paperformat_args,
            set_viewport_size=set_viewport_size,
        )
        report_sudo = self._get_report(report_ref)
        watermark = self._get_brand_watermark(report_sudo)
        if not watermark:
            return result
        return self._apply_brand_watermark(result, watermark, report_sudo)

    @api.model
    def _get_brand_watermark(self, report_sudo):
        """Return the decoded brand watermark of the first printed record."""
        if not (self.use_brand_watermark or report_sudo.use_brand_watermark):
            return None
        docids = self.env.context.get("res_ids")
        model_name = self.model or report_sudo.model
        if not docids or not model_name:
            return None
        record = self.env[model_name].browse(docids[:1])
        if "brand_id" not in record._fields:
            return None
        brand = record.brand_id
        if not brand.pdf_watermark:
            return None
        return b64decode(brand.pdf_watermark)

    @api.model
    def _load_brand_watermark_pdf(self, watermark, report_sudo):
        try:
            return PdfFileReader(BytesIO(watermark))
        except (UnicodeDecodeError, PdfReadError):
            # let's see if we can convert this with pillow
            try:
                Image.init()
                image = Image.open(BytesIO(watermark))
                pdf_buffer = BytesIO()
                if image.mode != "RGB":
                    image = image.convert("RGB")
                paperformat = (
                    self.paperformat_id
                    or report_sudo.paperformat_id
                    or self.env.company.paperformat_id
                )
                resolution = image.info.get("dpi", paperformat.dpi or 90)
                if isinstance(resolution, tuple):
                    resolution = resolution[0]
                image.save(pdf_buffer, "pdf", resolution=resolution)
                return PdfFileReader(pdf_buffer)
            except Exception:
                logger.exception("Failed to load brand watermark")
        return None

    @api.model
    def _apply_brand_watermark(self, result, watermark, report_sudo):
        """Put the first page of ``watermark`` underneath every page of ``result``.

        Any watermark already applied (e.g. the company watermark) is part of
        the page content at this point, so it ends up stacked on top of the
        brand watermark.
        """
        pdf_watermark = self._load_brand_watermark_pdf(watermark, report_sudo)
        if not pdf_watermark:
            logger.error("No usable brand watermark found, got %s...", watermark[:100])
            return result
        if not self.pdf_has_usable_pages(len(pdf_watermark.pages)):
            return result

        pdf = PdfFileWriter()
        add_blank_page = getattr(pdf, "add_blank_page", None) or pdf.addBlankPage
        for page in PdfFileReader(BytesIO(result)).pages:
            mediabox = getattr(page, "mediabox", None) or page.mediaBox
            # [llx, lly, urx, ury] works across all supported pypdf versions
            llx, lly, urx, ury = (float(v) for v in mediabox)
            watermark_page = add_blank_page(urx - llx, ury - lly)
            merge_page = (
                getattr(watermark_page, "merge_page", None) or watermark_page.mergePage
            )
            merge_page(pdf_watermark.pages[0])
            merge_page(page)

        pdf_content = BytesIO()
        pdf.write(pdf_content)
        return pdf_content.getvalue()
