# Copyright (C) 2025 Bosd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailTemplateExt(models.Model):
    _inherit = "mail.template"

    brand_id = fields.Many2one("res.brand", "Brand")
