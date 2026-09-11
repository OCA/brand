# Copyright 2024 CIT-Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo import _, models
from odoo.exceptions import UserError


class Report(models.Model):
    _inherit = "ir.actions.report"

    def _get_watermark(self, report_ref, docids=False):
        report_sudo = super()._get_report(report_ref)
        if docids and report_sudo.model and report_sudo.model in self.env:
            docs = self.env[report_sudo.model].browse(docids)

            if "brand_id" in docs._fields:
                distinct_brands = set(doc.brand_id for doc in docs)
                if len(distinct_brands) > 1:
                    no_brand_name = _("No Brand")
                    brand_names = ", ".join(
                        b.name if b else no_brand_name for b in distinct_brands
                    )
                    raise UserError(
                        _(
                            "Cannot print documents belonging to "
                            "different brands (%s) together."
                        )
                        % brand_names
                    )
                if docs:
                    brand = docs[0].brand_id
                    if brand and brand.pdf_watermark:
                        return base64.b64decode(brand.pdf_watermark)

        return super()._get_watermark(report_ref, docids=docids)
