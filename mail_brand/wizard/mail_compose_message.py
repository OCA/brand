from odoo import api, fields, models


class MailComposeMessageExt(models.TransientModel):
    _inherit = "mail.compose.message"

    brand_id = fields.Many2one(comodel_name="res.brand", string="Brand")

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        model = result.get("model")
        res_id = result.get("res_id")

        if model and res_id and "brand_id" in fields:
            model_object = self.env[model].browse(res_id)
            if hasattr(model_object, "brand_id") and model_object.brand_id:
                result["brand_id"] = model_object.brand_id.id
        else:
            result["brand_id"] = self.brand_id

        return result

    def action_send_mail(self):
        """Override to explicitly pass the brand_id in the context."""
        self.ensure_one()
        if self.brand_id:
            self = self.with_context(email_brand=self.brand_id.id)
        return super().action_send_mail()
