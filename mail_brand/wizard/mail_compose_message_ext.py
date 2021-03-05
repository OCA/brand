# Copyright 2021 Yves Goldberg
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MailComposeMessageExt(models.TransientModel):
    _inherit = "mail.compose.message"

    brand_id = fields.Many2one("brand", "Brand")

    @api.model
    def default_get(self, fields):
        result = super(MailComposeMessageExt, self).default_get(fields)
        model = result.get("model", False)
        res_id = result.get("res_id", False)
        if model and res_id:
            model_object = self.env[model].browse(res_id)
            if hasattr(model_object, "brand_id"):
                result["brand_id"] = model_object.brand_id.id
        return result
