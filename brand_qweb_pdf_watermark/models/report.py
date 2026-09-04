
from base64 import b64decode

from odoo import _, models
from odoo.exceptions import UserError


class Report(models.Model):
    _inherit = "ir.actions.report"

    def _get_watermark(self, report_ref, docids=False):
        report_sudo = self._get_report(report_ref)
        docs = None
        if docids and report_sudo.model and report_sudo.model in self.env:
            docs = self.env[report_sudo.model].browse(docids)

            if "brand_id" in docs._fields:
                distinct_brands = set(doc.brand_id for doc in docs)
                if len(distinct_brands) > 1:
                    brand_names = ", ".join(b.name if b else _("No Brand") for b in distinct_brands)
                    raise UserError(_("Cannot print documents belonging to different brands (%s) together.") % brand_names)
                for doc in docs:
                    if doc.brand_id and doc.brand_id.pdf_watermark:
                        return b64decode(doc.brand_id.pdf_watermark)

        return super()._get_watermark(report_ref, docids=docids)
