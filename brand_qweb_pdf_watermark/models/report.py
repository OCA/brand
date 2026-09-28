# Copyright 2026 CIT-Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo import _, models
from odoo.exceptions import UserError


class Report(models.Model):
    _inherit = "ir.actions.report"

    def _get_watermark(self, report_ref, docids=False):
        report_sudo = super()._get_report(report_ref)
        if "brand_id" in self.env[report_sudo.model]._fields:
            docs = self.env[report_sudo.model].browse(docids)
            brands = docs.mapped("brand_id")
            if len(brands) > 1:
                brand_names = ", ".join(brands.mapped("name"))
                raise UserError(
                    _(
                        "Cannot print documents belonging to "
                        "different brands (%s) together."
                    )
                    % brand_names
                )
            if brands and any(not doc.brand_id for doc in docs):
                raise UserError(
                    _("Some of the documents do not have a brand linked to it.")
                )
            brand = docs and docs[0].brand_id
            if brand and brand.pdf_watermark:
                return base64.b64decode(brand.pdf_watermark)

        return super()._get_watermark(report_ref, docids=docids)
