# Copyright 2024 CIT-Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo import _, api, models
from odoo.exceptions import UserError


class Report(models.Model):
    _inherit = "ir.actions.report"

    @api.model
    def _get_report(self, report_ref):
        report_sudo = super()._get_report(report_ref)
        if (
            not report_sudo
            or report_sudo.pdf_watermark
            or self.env.context.get("skip_brand_watermark")
        ):
            return report_sudo

        docids = self.env.context.get("res_ids")
        if not docids:
            return report_sudo

        watermark = self.with_context(skip_brand_watermark=True)._get_watermark(
            report_sudo, docids=docids
        )
        if watermark:
            b64_watermark = base64.b64encode(watermark)
            return report_sudo.new({"pdf_watermark": b64_watermark}, origin=report_sudo)

        return report_sudo

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
                for doc in docs:
                    if doc.brand_id and doc.brand_id.pdf_watermark:
                        return base64.b64decode(doc.brand_id.pdf_watermark)

        if hasattr(super(), "_get_watermark"):
            return super()._get_watermark(report_ref, docids=docids)
        return None
