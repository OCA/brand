# Copyright (C) 2022 Snakebyte
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def _notify_prepare_template_context(
        self, message, msg_vals, model_description=False, mail_auto_delete=True
    ):
        result = super()._notify_prepare_template_context(
            message, msg_vals, model_description, mail_auto_delete
        )

        result["has_brand"] = hasattr(self, "brand_id")
        if result["has_brand"]:
            result["company"] = self.brand_id
            if self.brand_id.website:
                result["website_url"] = (
                    "https://%s" % self.brand_id.website
                    if not self.brand_id.website.lower().startswith(("http:", "https:"))
                    else self.brand_id.website
                )
            else:
                result["website_url"] = False
        return result
