# Copyright (C) 2022 Snakebyte
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def _notify_prepare_template_context(
        self, message, msg_vals, model_description=False, mail_auto_delete=True
    ):
        result = super()._notify_prepare_template_context(
            message, msg_vals, model_description, mail_auto_delete
        )

        _logger.info(f"Context in _notify_prepare_template_context: {self.env.context}")
        brand = False
        # Retreive the brand when coming from mail compose wizard
        if self.env.context.get("email_brand"):
            brand = self.env["res.brand"].browse(self.env.context["email_brand"])
            result["company"] = brand.partner_id
            result["website_url"] = self._format_website_url(brand.partner_id.website)
            result["brand"] = brand
            result["has_brand"] = 1

        # Case where the model is branded
        if not brand and hasattr(self, "brand_id"):
            result["company"] = self.brand_id
            result["website_url"] = self._format_website_url(self.brand_id.website)
            result["brand"] = self.brand_id
            result["has_brand"] = 1
        return result

    def _format_website_url(self, website):
        if website:
            return (
                f"https://{website}"
                if not website.lower().startswith(("http:", "https:"))
                else website
            )
        return False
