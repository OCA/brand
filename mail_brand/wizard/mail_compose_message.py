from odoo import api, fields, models

from odoo.addons.mail.tools.parser import parse_res_ids


class MailComposeMessageExt(models.TransientModel):
    _inherit = "mail.compose.message"

    brand_id = fields.Many2one(comodel_name="res.brand", string="Brand")

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        if "brand_id" not in fields:
            return result

        # In v18 res_id (integer) was replaced by res_ids (Text, JSON list);
        # the chatter passes default_res_ids/default_model instead of active_id.
        model = result.get("model")
        res_ids_raw = result.get("res_ids")
        if model and res_ids_raw:
            res_ids = parse_res_ids(res_ids_raw, self.env)
            if res_ids:
                model_object = self.env[model].browse(res_ids[0])
                if hasattr(model_object, "brand_id") and model_object.brand_id:
                    result["brand_id"] = model_object.brand_id.id

        return result

    def action_send_mail(self):
        """Override to explicitly pass the brand_id in the context."""
        self.ensure_one()
        if self.brand_id:
            self = self.with_context(email_brand=self.brand_id.id)
        return super().action_send_mail()
